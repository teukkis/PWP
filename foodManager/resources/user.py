import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import User
from foodManager import db
from foodManager.utils.responsebuilder import ResponseBuilder
from foodManager.utils.masonbuilder import MasonBuilder
from foodManager.constants import *

class UserCollection(Resource):

    def get(self):
        users = User.query.all()
        body = MasonBuilder(items=[])
        for user in users:
            item = {"username": user.username,
                    "email": user.email}
            body["items"].append(item)
        return Response(json.dumps(body),status=200)

    def post(self):
        pass

class UserItem(Resource):

    def get(self, item):
        pass
    def put(self, item):
        pass
    def delete(self, item):
        pass
