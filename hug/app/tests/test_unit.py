import json
from unittest.mock import MagicMock, call

import falcon.testing
import hug
import pytest

import contact_list.app


@pytest.fixture
def mock_redis():
    return MagicMock()


@pytest.fixture
def test_client(mock_redis):
    hug_api = contact_list.app.create_api(mock_redis)
    return falcon.testing.TestClient(hug_api.http.server())


def test_get_contact(mock_redis, test_client):
    fake_uuid = 'asd'
    fake_contact = {"something": "whatever"}
    mock_redis.get.return_value = json.dumps(fake_contact).encode()

    resp = test_client.simulate_get('/contacts/{}'.format(fake_uuid))

    assert resp.status == hug.HTTP_200
    assert resp.json == fake_contact
    assert call(fake_uuid) in mock_redis.get.mock_calls


def test_post_malformed_contact(test_client):
    resp = test_client.simulate_post('/contacts',
                                     headers={'content-type': 'application/json'},
                                     body=json.dumps({'something': 'whatever'}))
    assert resp.status == hug.HTTP_400


# TODO fails when run with other tests because of a bug in Hug?
def test_post_contact(mock_redis, test_client, monkeypatch):
    contact = {
        'name': 'John Smith',
        'phone': {
            'mobile': '666-666-666',
            'work': '777-777-777',
        },
        'email': [
            'john@smith',
            'johnsmith@example.com',
        ]
    }
    fake_uuid = 'blablabla'
    contact_with_id = contact.copy()
    contact_with_id['id'] = fake_uuid
    monkeypatch.setattr('contact_list.app.uuid.uuid4', lambda: fake_uuid)

    resp = test_client.simulate_post('/contacts',
                                     headers={'content-type': 'application/json'},
                                     body=json.dumps(contact))

    assert resp.status == hug.HTTP_201
    assert resp.json == contact_with_id
    assert call(fake_uuid, json.dumps(contact_with_id)) in mock_redis.set.mock_calls
