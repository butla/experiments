from pathlib import Path

import psycopg2

from . import db


def main():
    schema_setup_sql = (Path(__file__).parent / 'schema_setup.sql').absolute().read_text()

    connection = db.create_connection()
    cursor = connection.cursor()
    cursor.execute(schema_setup_sql)
    # TODO get the stdout from the command
    print('Schema created.')


if __name__ == '__main__':
    main()
