import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import User
from foodManager import db
from foodManager.utils import responseBuilder
from foodManager.constants import *

class Users(Resource):

    def get(self):
        return Response("All users..",status=200)
    def post(self):
        pass

class User(Resource):

    def get(self, item):
        pass
    def put(self, item):
        pass
    def delete(self, item):
        pass
