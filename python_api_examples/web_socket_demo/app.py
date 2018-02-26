import tornado.httpserver
import tornado.gen
import tornado.ioloop
import tornado.websocket

import os


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

    # so we accept connections on ws:// and not send 403
    def check_origin(self, origin):
        return True


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", EchoWebSocket),
    ])
    port = int(os.getenv('VCAP_APP_PORT', '9090')) 

    application.listen(port)
    tornado.ioloop.IOLoop.current().start()
