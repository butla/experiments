import psycopg2

from . import config

SQL = """
CREATE TABLE IF NOT EXISTS groups(
    id SERIAL PRIMARY KEY,
    item_label_counts JSONB
);

CREATE TABLE IF NOT EXISTS items(
    id SERIAL PRIMARY KEY,
    label TEXT,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups
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
    print('Schema created.')


if __name__ == '__main__':
    main()
