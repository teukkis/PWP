import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import User
from foodManager import db
from foodManager.utils.responsebuilder import ResponseBuilder, create_error_response
from foodManager.utils.masonbuilder import MasonBuilder

from foodManager.constants import *

class Entry(Resource):
    
    def get(self):
        body = ResponseBuilder()
        body.add_namespace("foodman", "/foodmanager/link-relations/")
        body.add_control_add_user()
        body.add_control_get_users()
        
        return Response(json.dumps(body), status=200, mimetype=MASON)