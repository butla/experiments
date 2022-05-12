import asyncio
import json

from aiohttp import web
import uvloop


async def handle_get(request):
    # schedule something to run in the background
    # asyncio.get_event_loop().create_task(background_stuff())
    return web.Response(text='Hello, world')


async def handle_post(request):
    if request.content_type != 'application/json':
        raise web.HTTPUnsupportedMediaType(text='Media type needs to be application/json')
    body_json = await request.json() 
    resp_json = {key: value for key, value in body_json.items() if key.lower().startswith('a')}
    return web.Response(
            text=json.dumps(resp_json),
            content_type='application/json')


def init_app():
    app = web.Application()
    app.router.add_route('GET', '/', handle_get)
    app.router.add_route('POST', '/', handle_post)
    # app.router.add_route('GET', '/{name}', handle)
    return app


async def background_stuff():
    await asyncio.sleep(5)
    print("5 seconds passed since a call...")


if __name__ == '__main__':
    uvloop.install()
    app = init_app()
    web.run_app(app, port=9090)
