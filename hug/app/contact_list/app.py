import os
import uuid

import hug
from marshmallow import Schema, fields
import redis


class Contact(Schema):
    email = fields.List(fields.Str())
    name = fields.Str()
    phone = fields.Dict()


redis_client = redis.Redis(port=os.getenv('REDIS_PORT', 6379))


@hug.post('/contacts', status=hug.HTTP_201)
def create_contact(body: hug.types.MarshmallowSchema(Contact()), response):
    contact = body
    contact_id = str(uuid.uuid4())
    contact['id'] = contact_id

    redis_client.hmset(contact_id, contact)

    response.location = '/contacts/' + contact_id
    return contact


@hug.get('/contacts/{id}')
def get_contact(id: hug.types.text):
    return redis_client.hgetall(id)

# def get_app():
#     api = hug.API(__name__)
#     hug.post('/contacts', api=api)(create_contact)
#     return api.http.server()