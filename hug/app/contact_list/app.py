import json
import os
import uuid

import hug
from marshmallow import Schema, fields
import redis


class Contact(Schema):
    email = fields.List(fields.Str())
    name = fields.Str(required=True)
    phone = fields.Dict()


class ContactList:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def create_contact(self, response, body: hug.types.MarshmallowSchema(Contact())):
        contact = body
        contact_id = str(uuid.uuid4())
        contact['id'] = contact_id

        self.redis_client.set(contact_id, json.dumps(contact))

        response.location = '/contacts/' + contact_id
        return contact

    def get_contact(self, id: hug.types.text):
        return self.redis_client.get(id)


@hug.format.content_type('application/json')
def json_from_bytes(content, request=None, response=None, **kwargs):
    return content


def create_api(redis_client):
    contacts = ContactList(redis_client)
    api = hug.API(__name__)

    hug.post('/contacts', status=hug.HTTP_201, api=api)(contacts.create_contact)
    hug.get('/contacts/{id}', output=json_from_bytes, api=api)(contacts.get_contact)

    return api


def get_app():
    redis_client = redis.Redis(port=os.getenv('REDIS_PORT', 6379))
    api = create_api(redis_client)
    return api.http.server()