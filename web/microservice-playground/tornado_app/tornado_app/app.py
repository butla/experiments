import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.web


class SampleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    # TODO change to coroutine?
    def post(self):
        body_json = tornado.escape.json_decode(self.request.body)
        self.write({key: value for key, value in body_json.items() if key.lower().startswith('a')})


application = tornado.web.Application([
    (r"/", SampleHandler),
])

if __name__ == "__main__":
    # # single core
    # application.listen(9090)
    # tornado.ioloop.IOLoop.current().start()

    # multicore example
    server = tornado.httpserver.HTTPServer(application)
    server.bind(9090)
    server.start(0)  # autodetect number of cores and fork a process for each
    tornado.ioloop.IOLoop.instance().start()
