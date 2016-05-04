import falcon
import json
import jwt
import os
import requests
from pymongo import MongoClient

CONTEXT_USER = 'user_name'


class Authenticator:
    def __init__(self):
        uaa_response = requests.get('https://uaa.gotapaas.eu/token_key')
        self._uaa_public_key = uaa_response.json()['value']
        # we should get that and translate from uaa)response, but this is a short demo
        self._key_alg = 'RS256'

    def authenticate(self, req, resp, resource, params):
        if not req.auth:
            raise falcon.HTTPUnauthorized(
                'Authorization required',
                'Put CF Oauth2 token in Authorization header')

        # we don't need the 'bearer ' header
        token = req.auth.split()[1]
        try:
            token_payload = jwt.decode(token,
                                       key=self._uaa_public_key,
                                       verify=True,
                                       algorithms=[self._key_alg],
                                       audience="cloud_controller")
        except jwt.DecodeError:
            raise falcon.HTTPUnauthorized(
                'Invalid authorization token',
                'Something is wrong with your token')

        req.context[CONTEXT_USER] = token_payload['user_name']


authenticator = Authenticator()


@falcon.before(authenticator.authenticate)
class DocStoreResource:
    MONGO_COLLECTION_NAME = 'user-docs'
    USER_LABEL = 'user'

    def __init__(self):
        services_config = json.loads(os.environ['VCAP_SERVICES'])
        credentials = services_config['mongodb26'][0]['credentials']

        mongo_client = MongoClient(
            host=credentials['hostname'],
            port=int(credentials['port'])
        )
        db = mongo_client[credentials['dbname']]
        db.authenticate(credentials['username'], credentials['password'])

        self._collection = db[self.MONGO_COLLECTION_NAME]

    def on_get(self, req, resp):
        user_docs = self._collection.find({self.USER_LABEL: req.context[CONTEXT_USER]})

        merged_docs = []
        for doc in user_docs:
            # ObjectId from MongoDB isn't serializable to JSON and we don't want to define a new encoder
            del doc['_id']
            merged_docs.append(doc)

        resp.body = json.dumps({'user_docs': merged_docs})

    def on_post(self, req, resp):
        doc = json.loads(req.stream.read().decode('utf-8'))
        doc[self.USER_LABEL] = req.context[CONTEXT_USER]

        self._collection.insert_one(doc)

        resp.body = 'Document added'
        resp.status = falcon.HTTP_201


application = falcon.API()
application.add_route('/', DocStoreResource())
