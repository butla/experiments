# TODO:
# - insert
# - update
# - 0 updates
# - multiple inserts
# - delete - just error out?

import pytest
from triggers import repository


def test_run_an_sql_function(db_cursor):
    bag_id = repository.create_bag(db_cursor)
    items_to_add = ['square'] + (['round'] * 2) + (['squiggly'] * 3)
    repository.create_items(items_to_add, bag_id, db_cursor)

    db_cursor.execute('select bag_items_count(%s)', (bag_id,))
    bag_item_counts = db_cursor.fetchone()[0]

    assert bag_item_counts == {"round": 2, "square": 1, "squiggly": 3}
