import enum
import functools
import subprocess

import networkx
from networkx.drawing.nx_pydot import write_dot

def create_label(trigger, outputs=None):
    if not outputs:
        return trigger
    outputs_in_brackets = [f'({output})' for output in outputs]
    outputs_part_of_label = '\n'.join(outputs_in_brackets)
    return f'{trigger}\n{outputs_part_of_label}'


def add_transition(graph, from_state, action, to_state, *outputs):
    graph.add_edge(from_state, to_state, label=create_label(action, outputs))



def create_uploader_graph() -> networkx.DiGraph:
    # We're using a directed multigraph, because the mathematical definition of a graph
    # doesn't allow for multiple edges between the same nodes, and we need that to model
    # the state machine fully.
    g = networkx.MultiDiGraph()
    transition = functools.partial(add_transition, g)

    sd = 'STOPPED'
    w = 'WAITING'
    u = 'UPLOADING'
    sg = 'STOPPING'
    invalid = 'INVALID/ERROR'
    states = [sd, w, u, sg, invalid]

    # triggers or inputs, or actions
    add_event = 'add event'
    add_event_queue_full = 'add event, batch full'
    start = 'start'
    stop = 'stop'
    upload_finished = 'upload finished'
    interval_over = 'interval over'
    triggers = [add_event, add_event_queue_full, start, stop, upload_finished, interval_over]

    # outputs or side effects
    upload = 'upload'
    schedule_upload = 'schedule upload'
    cancel_scheduled = 'cancel scheduled upload'
    outputs = [upload, schedule_upload, cancel_scheduled]

    transition(sd, start, w, schedule_upload)

    transition(w, add_event_queue_full, u, upload, cancel_scheduled)
    transition(w, interval_over, u, upload)
    transition(w, stop, sg, upload, cancel_scheduled)

    transition(u, stop, sg)
    transition(u, upload_finished, w, schedule_upload)

    transition(sg, upload_finished, sd)
    transition(sg, add_event, invalid)
    #g.add_nodes_from(states)
    #g.add_edge(sd, w, label=create_label(start, [schedule_upload]))
    #g.add_edge(sd, invalid, label=create_label(interval_over))
    #g.add_edge(w, w, label=create_label(start))

    #g.add_edge(u, w, label='upload finished\n(dupa)\n(kupa)')
    #g.add_edge(u, sg, label='stop')
    #g.add_edge(sg, sd, label='upload finished')
    return g


def draw_graph(graph):
    graph_file = 'graph.dot'
    graph_pdf_file = 'graph.pdf'
    write_dot(graph, graph_file)
    subprocess.check_output(f'dot -Tpdf {graph_file} -o {graph_pdf_file}'.split())
    subprocess.check_output(f'okular {graph_pdf_file}'.split())

if __name__ == '__main__':
    draw_graph(create_uploader_graph())
