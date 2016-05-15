import falcon

class SampleResource:
    @staticmethod
    def on_get(req, resp):
        resp.body = 'some test response\n'

app = falcon.API()
app.add_route('/', SampleResource())

