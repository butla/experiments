# TODO:
# - insert
# - update
# - 0 updates
# - multiple inserts

import pytest
from psycopg2.extras import execute_values

from .db import create_connection


@pytest.fixture
def db_connection():
    return create_connection()


def test_insert_into_db(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO bags DEFAULT VALUES RETURNING id')
    bag_id = cursor.fetchone()[0]

    items_to_add = ['square'] + (['round'] * 2) + (['squiggly'] * 3)
    execute_values(
        cursor,
        'INSERT INTO items (kind, bag_id) VALUES %s',
        [(item, bag_id) for item in items_to_add],
    )

    cursor.execute('SELECT count(*) FROM items WHERE bag_id = %s', (bag_id,))
    assert cursor.fetchone()[0] == len(items_to_add)


def test_try_the_trigger_function():
    cursor = db_connection.cursor()
    cursor.execute('INSERT INTO bags DEFAULT VALUES RETURNING id')
    bag_id = cursor.fetchone()[0]

    items_to_add = ['square'] + (['round'] * 2) + (['squiggly'] * 3)
    execute_values(
        cursor,
        'INSERT INTO items (kind, bag_id) VALUES %s',
        [(item, bag_id) for item in items_to_add],
    )

    # TODO insert counts into the bag with a function that will be a part of the trigger
