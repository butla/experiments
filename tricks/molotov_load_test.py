from molotov import scenario


@scenario(100)
async def local_hello_world(session):
    async with session.get('http://localhost:9090') as resp:
        assert resp.status == 200
        text = await resp.text()
        assert text == 'Hello, world'

