import pytest
from triggers.db import create_connection


@pytest.fixture(scope='module')
def db_connection():
    return create_connection()


@pytest.fixture
def db_cursor(db_connection):
    return db_connection.cursor()
