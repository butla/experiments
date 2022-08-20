from triggers import repository


def test_insert_items_into_a_bag(db_cursor):
    bag_id = repository.create_bag(db_cursor)

    items_to_add = ['square'] + (['round'] * 2) + (['squiggly'] * 3)
    repository.create_items(items_to_add, bag_id, db_cursor)

    db_cursor.execute('SELECT count(*) FROM items WHERE bag_id = %s', (bag_id,))
    assert db_cursor.fetchone()[0] == len(items_to_add)
