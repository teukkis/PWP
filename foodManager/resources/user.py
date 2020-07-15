import json from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from food_manager.models import Users, User
from food_manager import db
from food_manager.utils import ResponseBuilder
from food_manager.constants import *

class Users(Resource):

    def get(self):

    def post(self):


class User(Resource):

    def get(self, item):

    def put(self, item):

    def delete(self, item):

