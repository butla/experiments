import os
import sys
from urllib.parse import urljoin
import uuid

import mountepy
import pytest
import requests


def dict_contains(dict_a, dict_b):
    """Checks if A contains B"""
    return dict_a.items() >= dict_b.items()


@pytest.yield_fixture(scope='session')
def contact_app():
    waitress_path = os.path.join(os.path.dirname(sys.executable), 'waitress-serve')
    app_command = [
        waitress_path,
        '--port', '{port}',
        # '--call', 'contact_list.app:__hug_wsgi__']
        'contact_list.app:__hug_wsgi__']

    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    project_root_path = os.path.join(this_file_dir, '..')
    contact_service = mountepy.HttpService(
        app_command,
        env={'PYTHONPATH': project_root_path})

    contact_service.start()
    yield contact_service
    contact_service.stop()

# TODO pytest-docker-pexpect for redis


def test_store_and_get_contact(contact_app):
    contact = {
        'name': 'John Smith',
        'phone': {
            'mobile': '666-666-666',
            'work': '777-777-777',
        },
        'email': [
            'john@smith',
            'johnsmith@example.com',
        ]
    }

    post_resp = requests.post(urljoin(contact_app.url, '/contacts'), json=contact)

    assert post_resp.status_code == 201
    assert dict_contains(post_resp.json(), contact)
    try:
        uuid.UUID(post_resp.json()['id'])
    except ValueError:
        pytest.fail('The returned contact ID was not a valid UUID.')

    get_resp = requests.get(urljoin(contact_app.url, post_resp.headers['location']))

    assert get_resp.json() == post_resp.json()

# TODO get HTML
# TODO merge contacts?