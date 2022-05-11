from functools import partial
import json
import logging
import typing

from aiohttp import web
import aredis
import env_var_config

SAVE_FUNCTION_KEY = 'savorado'


async def hello(request: web.Request):
    name = request.match_info.get('name', 'Señor Incognito')
    await (request.app[SAVE_FUNCTION_KEY](name))
    return json_response({'greeting': f'Hello, {name}!'})


# functional programming, yay!
json_response = partial(
    web.json_response,
    dumps=partial(json.dumps, ensure_ascii=False),
)


class AppConfig(typing.NamedTuple):
    port: int
    redis_host: str
    redis_port: int
    names_collection: str = 'names'


def create_app(saver):
    app = web.Application()
    app.add_routes([
        web.get('/hello/{name}', hello),
        web.get('/hello', hello),
    ])
    app[SAVE_FUNCTION_KEY] = saver

    return app


def run_server():
    logging.basicConfig(level=logging.INFO)

    config = env_var_config.gather_config_for_class(AppConfig)
    redis = aredis.StrictRedis(
        host=config.redis_host,
        port=config.redis_port,
    )
    save_name = partial(redis.lpush, config.names_collection)

    app = create_app(saver=save_name)
    web.run_app(app, port=config.port)


if __name__ == '__main__':
    run_server()
