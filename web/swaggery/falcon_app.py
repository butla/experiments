import falcon
import json

class SampleResource:
    @staticmethod
    def on_get(req, resp, some_num):
        resp_dict = {'a': some_num, 'b': some_num + 'sraka'}
        resp.body = json.dumps(resp_dict)

app = falcon.API()
app.add_route('/{some_num}', SampleResource())

