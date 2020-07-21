import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import ShoppingList, ShoppingListFoodItem
from foodManager import db
from foodManager.utils.responsebuilder import ResponseBuilder
from foodManager.constants import *


class ShoppingListCollection(Resource):

    def get(self):
        pass
    def post(self):
        pass
    def delete(self):
        pass

class ShoppingListItem(Resource):

    def get(self, item):
        pass
    def put(self, item):
        pass
    def delete(self, item):
        pass
