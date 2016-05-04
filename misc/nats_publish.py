import pynats

nats_url = 'nats://nats:natspass@localhost:4222'

conn = pynats.Connection(nats_url)
conn.connect()

conn.ping()

conn.publish('foo', 'srakaptaka')
