import uuid

import hug
from marshmallow import Schema, fields


class Contact(Schema):
    email = fields.List(fields.Str())
    name = fields.Str()
    phone = fields.Dict()


@hug.post('/contacts', status=hug.HTTP_201)
def create_contact(body: hug.types.MarshmallowSchema(Contact()), response):
    contact_id = str(uuid.uuid4())
    body['id'] = contact_id
    response.location = '/contacts/' + contact_id
    return body


# def get_app():
#     api = hug.API(__name__)
#     hug.post('/contacts', api=api)(create_contact)
#     return api.http.server()

# TODO put redis address