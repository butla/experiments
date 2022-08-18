import psycopg2

from . import config


# TODO retry
def create_connection():
    connection = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
    )
    connection.autocommit = True
    return connection
