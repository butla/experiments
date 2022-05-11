from collections import defaultdict
from functools import partial
import json
import logging
import os.path
import pprint
from typing import Dict, Collection, List, Optional
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, quote

from dataclasses import dataclass
import requests

_log = logging.getLogger(__name__)


# TODO replace with CLI arguments
KEY = 'TODO'
TOKEN = 'TODO'

def _trello_call(path: str, key: str, token: str, method: str = 'GET'):
    url = urljoin(
        'https://api.trello.com',
        os.path.join('/1', path),
    )
    method_function = getattr(requests, method.lower())
    final_url = merge_url_query_params(url, {'key': KEY, 'token': TOKEN})
    _log.debug('URL called: %s', final_url)
    # TODO put an issue in pylint?
    # what will happen when I install pylint in here?
    resp = method_function(final_url)  # pylint: disable=not-callable
    resp.raise_for_status()
    return resp.json()

trello_call = partial(_trello_call, key=KEY, token=TOKEN)


@dataclass(frozen=True)
class TrelloBoard:
    name: str
    id_: str


# But this is exactly the same body as for the Board! Yes! But it doesn't take long to write at
# all but gives us a clear description of a different context!
# Maybe that's not how you should code always, but hey! here it works.
@dataclass(frozen=True)
class TrelloList:
    name: str
    id_: str


# We're relaying immediately what we are returning and how it looks like.
# IDE's and REPLs will help write code using this code.
def get_boards() -> List[TrelloBoard]:
    boards = trello_call('members/me/boards')
    return [TrelloBoard(board['name'], board['id'])
            for board in boards
            if not board['closed']]


@dataclass(frozen=True)
class WunderlistSubtask:
    title: str
    completed: bool


@dataclass(frozen=True)
class WunderlistTask:
    id_: int
    title: str
    completed: bool
    subtasks: List[WunderlistSubtask]
    note: str


def get_boards_lists(boards: Collection[TrelloBoard]) -> List[TrelloList]:
    lists = []
    for board in boards:
        data = trello_call(f'boards/{board.id_}/lists')
        boards_lists = [TrelloList(list_['name'], list_['id']) for list_ in data]
        lists.extend(boards_lists)
    return lists


# TODO this is the export file, should be replaced with an argument
def get_wunderlist_data():
    with open('/home/butla/development/wunderlist-20180915-12_01_56.json', 'r') as f:
        wunderlist = json.load(f)
    return wunderlist['data']


def get_wunderlist_tasks_per_list(wunderlist_data: dict) -> Dict[str, WunderlistTask]:
    task_ids_to_notes = {note['task_id']: note['content']
                         for note in wunderlist_data['notes']}

    task_ids_to_subtasks = defaultdict(list)
    for subtask in wunderlist_data['subtasks']:
        tasks_subtasks = task_ids_to_subtasks[subtask['task_id']]
        tasks_subtasks.append(
            WunderlistSubtask(
                title=subtask['title'],
                completed=subtask['completed'],
            )
        )

    list_ids_to_names = {list_['id']: list_['title']
                         for list_ in wunderlist_data['lists']}

    tasks_per_list_id = defaultdict(list)
    for task in wunderlist_data['tasks']:
        task_id = task['id']
        task_list = tasks_per_list_id[task['list_id']]
        task_list.append(
            WunderlistTask(
                id_=task_id,
                title=task['title'],
                completed=task['completed'],
                subtasks=task_ids_to_subtasks.get(task_id, []),
                note=task_ids_to_notes.get(task_id, ''),
            )
        )
    return {list_ids_to_names[id_]: list_ for id_, list_ in tasks_per_list_id.items()}


def trello_card_from_wunderlist_task(task: WunderlistTask, target_list_id: str):
    _log.info('Uploading card %s', task.id_)
    quoted_description = quote(task.note)
    card_response = trello_call(
        f'cards?idList={target_list_id}&name={task.title}&desc={quoted_description}',
        method='POST',
    )
    card_id = card_response['id']
    if task.subtasks:
        _log.info('Creating a checklist for Wunderlist task %s', task.id_)
        checklist_id = trello_call(
            f'cards/{card_id}/checklists?name=TODO',
            method='POST',
        )['id']
        for subtask in task.subtasks:
            _log.info('Creating a subtask for Wunderlist task %s', task.id_)
            api_friendly_checked_value = str(subtask.completed).lower()
            trello_call(
                (f'checklists/{checklist_id}/checkItems'
                 f'?name={subtask.title}&checked={api_friendly_checked_value}'),
                method='POST',
            )
    if task.completed:
        trello_call(f'cards/{card_id}?closed=true', method='PUT')


# I put that on Stack Overflow https://stackoverflow.com/a/52373377/2252728
def merge_url_query_params(url: str, additional_params: dict) -> str:
    url_components = urlparse(url)
    original_params = parse_qs(url_components.query)
    # Before Python 3.5 you could update original_params with additional_params, but here
    # all the variables are immutable.
    merged_params = {**original_params, **additional_params}
    updated_query = urlencode(merged_params, doseq=True)
    return url_components._replace(query=updated_query).geturl()


def main():
    logging.basicConfig(level=logging.INFO)

    wunderlist_to_trello_list_names = {
        'Życie': 'Długoterminowe',
        'Technologie i narzędzia': 'Narzędzia',
        'Kodzenie': 'Python',
        'Nauka': 'Czytanie - długie',
        'Sprzątanie itp.': 'Cykliczne',
        'Robota': 'Projekty / pomysły',
        'Pakowanie': 'Pakowanie',
    }
    trello_boards = get_boards()
    trello_lists = get_boards_lists(trello_boards)
    trello_list_names_to_ids = {list_.name: list_.id_ for list_ in trello_lists}

    wunderlist_data = get_wunderlist_data()
    wunderlist_tasks = get_wunderlist_tasks_per_list(wunderlist_data)

    trello_list_ids_to_wunderlist_tasks = {}
    for wunderlist_list_name, task_list in wunderlist_tasks.items():
        trello_list_name = wunderlist_to_trello_list_names.get(wunderlist_list_name)
        if not trello_list_name:
            continue
        trello_list_id = trello_list_names_to_ids[trello_list_name]
        trello_list_ids_to_wunderlist_tasks[trello_list_id] = task_list

    for trello_list_id, task_list in trello_list_ids_to_wunderlist_tasks.items():
        for task in task_list:
            trello_card_from_wunderlist_task(task, trello_list_id)

if __name__ == '__main__':
    main()
