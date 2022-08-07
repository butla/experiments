import psycopg2

from . import config

SQL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS bags(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_kind_counts JSONB
);

-- create type if it doesn't exist
DO $$ BEGIN
    IF to_regtype('item_kind') IS NULL THEN
        CREATE TYPE item_kind AS ENUM ('round', 'square', 'squiggly', 'other');
    ELSE
        raise notice 'item_kind type already exists, so not creating...';
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS items(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    kind item_kind,
    group_id integer REFERENCES bags (id)
);
"""


def main():
    connection = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
    )
    connection.autocommit = True

    cursor = connection.cursor()
    cursor.execute(SQL)
    # TODO get the stdout from the command
    print('Schema created.')


if __name__ == '__main__':
    main()
