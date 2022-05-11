import pytest
from awesome_server.server import create_app


@pytest.fixture
async def app_client(aiohttp_client):
    app = create_app(saver=_fake_save)
    return await aiohttp_client(app)


async def _fake_save(_):
    pass


async def test_hello_works(app_client):
    name = 'Wieńczysław'
    response = await app_client.get(f'/hello/{name}')

    assert response.status == 200
    response_json = await response.json()
    assert name in response_json['greeting']
