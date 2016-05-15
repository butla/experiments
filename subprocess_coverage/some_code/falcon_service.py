import falcon
import sys

class SampleResource:
    @staticmethod
    def on_get(req, resp):
        resp.body = 'some test response\n'
        
        current_executable = sys.argv[0]
        print(current_executable)
        if 'waitress' in current_executable:
            print('running on waitress')
        elif 'uwsgi' in current_executable:
            print('running on uwsgi')
        elif 'gunicorn' in current_executable:
            print('running on gunicorn')


app = falcon.API()
app.add_route('/', SampleResource())

