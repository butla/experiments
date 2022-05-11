import pytest

from fara import items


def test_serialize_date():
    assert items._serialize_date('01/14/1955') == 'ISODate("1955-01-14T00:00:00Z")'
