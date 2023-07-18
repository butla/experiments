import pynats

nats_url = 'nats://nats:natspass@localhost:4222'

conn = pynats.Connection(nats_url)
conn.connect()

conn.ping()

def callback(msg):
    print('Message received: {}'.format(msg.data))

conn.subscribe('foo', callback)
conn.wait(count=1)
