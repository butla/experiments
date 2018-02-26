import falcon


class SampleResource:
    def on_get(self, req, resp):
        resp.body = 'Hello world\n'


application = falcon.API()
application.add_route('/', SampleResource())
