from typing import List

from psycopg2.extras import execute_values


# TODO these should get a new connection from a pool in a contextvar
def create_items(kinds_for_items: List['str'], bag_id: str, cursor):
    execute_values(
        cursor,
        'INSERT INTO items (kind, bag_id) VALUES %s',
        [(item, bag_id) for item in kinds_for_items],
    )


def create_bag(cursor) -> str:
    cursor.execute('INSERT INTO bags DEFAULT VALUES RETURNING id')
    return cursor.fetchone()[0]
