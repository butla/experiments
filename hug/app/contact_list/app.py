import json
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

    redis_client.set(contact_id, json.dumps(contact))

    response.location = '/contacts/' + contact_id
    return contact


@hug.format.content_type('application/json')
def json_from_bytes(content, request=None, response=None, **kwargs):
    """JSON (Javascript Serialized Object Notation)"""
    return content


@hug.get('/contacts/{id}', output=json_from_bytes)
def get_contact(id: hug.types.text):
    return redis_client.get(id)

# def get_app():
#     api = hug.API(__name__)
#     hug.post('/contacts', api=api)(create_contact)
#     return api.http.server()