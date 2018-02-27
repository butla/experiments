import enum
import functools
import shlex
import subprocess
from typing import List

import networkx
from networkx.drawing.nx_pydot import write_dot

def create_label(trigger, outputs: List = None):
    if not outputs:
        return trigger
    outputs_in_brackets = [f'({output})' for output in outputs]
    outputs_part_of_label = '\n'.join(outputs_in_brackets)
    return f'{trigger}\n{outputs_part_of_label}'


def add_transition(graph, from_state, action, to_state, *outputs):
    graph.add_edge(from_state, to_state, label=create_label(action, outputs))


class StateMachine:
    """
    A representation of a state machine. Can be used to produce a graph of it.
    """

    def __init__(self, name='state_machine'):
        self._name = name
        # We're using a directed multigraph, because the mathematical definition of a graph
        # doesn't allow for multiple edges between the same nodes, and we need that to model
        # the state machine fully.
        self._graph = networkx.MultiDiGraph()

    # TODO this should take strings or enums
    def add_transition(self, from_state, action, to_state, *outputs):
        self._graph.add_edge(from_state, to_state, label=self._create_label(action, outputs))

    def dump_graph(self) -> str:
        """Dumps both as a dot file and as a svg.

        Returns:
            Name of the file with a displayable graph.
        """
        graph_dot_file = f'{self._name}.dot'
        graph_diagram_file = f'{self._name}.svg'
        write_dot(self._graph, graph_dot_file)
        subprocess.check_output(
            shlex.split(f'dot -Tsvg {graph_dot_file} -o {graph_diagram_file}')
        )
        return graph_diagram_file

    def show_graph(self):
        """Requires gwenview right now.
        """
        graph_file = self.dump_graph()
        subprocess.check_output(shlex.split(f'gwenview {graph_file}'))

    @staticmethod
    def _create_label(trigger, outputs: List = None):
        if not outputs:
            return trigger
        outputs_in_brackets = [f'({output})' for output in outputs]
        outputs_part_of_label = '\n'.join(outputs_in_brackets)
        return f'{trigger}\n{outputs_part_of_label}'


def draw_uploader_graph() -> networkx.DiGraph:
    # states
    stopped = 'STOPPED'
    upload_scheduled = 'UPLOAD_SCHEDULED'
    uploading = 'UPLOADING'
    uploading_before_stop = 'UPLOADING_BEFORE_STOP'

    # triggers or inputs, or actions
    add_event = 'add event'
    add_event_queue_full = 'add event, batch full'
    start = 'start'
    stop = 'stop'
    upload_finished = 'upload finished'
    interval_over = 'interval over'

    # outputs or side effects
    upload = 'upload'
    schedule_upload = 'schedule upload'
    cancel_scheduled = 'cancel scheduled upload'
    throw_error = 'throw error'

    m = StateMachine('uploader')
    m.add_transition(stopped, start, upload_scheduled, schedule_upload)

    m.add_transition(upload_scheduled, add_event_queue_full, uploading, upload, cancel_scheduled)
    m.add_transition(upload_scheduled, interval_over, uploading, upload)
    m.add_transition(upload_scheduled, stop, uploading_before_stop, upload, cancel_scheduled)

    m.add_transition(uploading, stop, uploading_before_stop)
    m.add_transition(uploading, upload_finished, upload_scheduled, schedule_upload)

    m.add_transition(uploading_before_stop, upload_finished, stopped)
    m.add_transition(uploading_before_stop, add_event, uploading_before_stop, throw_error)

    m.show_graph()


def draw_buffer_graph() -> networkx.DiGraph:
    # triggers or inputs, or actions
    take_batch = 'take_batch'
    delete_batch = 'delete_batch'
    add = 'add'
    add_full_batch = 'add, full batch ready'
    add_buffer_full = 'add, buffer full'

    # states
    neutral = 'NEUTRAL'
    batch_taken = 'BATCH TAKEN'
    invalid = 'INVALID/ERROR'

    # outputs or side effects
    notify_batch_ready = 'notify batch ready'
    clear_out_succesfull_events = 'delete succesfull events'
    drop_new_event = 'drop new event'
    mark_batch_for_deletion = 'mark batch for deletion'

    m = StateMachine('events_buffer')
    m.add_transition(neutral, take_batch, batch_taken, mark_batch_for_deletion)
    m.add_transition(neutral, add_full_batch, neutral, notify_batch_ready)
    m.add_transition(neutral, add_buffer_full, neutral, drop_new_event)
    m.add_transition(neutral, delete_batch, invalid)

    m.add_transition(batch_taken, take_batch, batch_taken, mark_batch_for_deletion)
    m.add_transition(batch_taken, add_buffer_full, batch_taken, drop_new_event)
    m.add_transition(batch_taken, delete_batch, neutral, clear_out_succesfull_events)

    m.show_graph()

if __name__ == '__main__':
    draw_uploader_graph()
    draw_buffer_graph()
