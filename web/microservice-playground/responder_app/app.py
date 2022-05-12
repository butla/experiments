import logging

import responder

api = responder.API()


class SampleResource:
    async def on_get(self, req, resp, *, who):
        who = who if who else 'world'
        resp.text = {'hello': who}


class BenchmarkResource:
    async def on_get(self, req, resp):
        resp.text = 'Hello, world'


if __name__ == '__main__':
    api.add_route('/{who}', SampleResource)
    api.add_route('/', BenchmarkResource)
    api.run(port=9090, log_level=logging.WARNING)
    # with logging
    # api.run(port=9090)
