from pathlib import Path

import psycopg2

from . import config


def main():
    # TODO retry
    connection = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
    )
    connection.autocommit = True

    schema_setup_sql = (Path(__file__).parent / 'schema_setup.sql').absolute().read_text()

    cursor = connection.cursor()
    cursor.execute(schema_setup_sql)
    # TODO get the stdout from the command
    print('Schema created.')


if __name__ == '__main__':
    main()
