import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import User
from foodManager import db
from foodManager.utils.responsebuilder import ResponseBuilder
from foodManager.utils.masonbuilder import UserBuilder, create_error_response
from foodManager.constants import *

class UserCollection(Resource):

    def get(self):
        body = UserBuilder(items=[])
        body.add_namespace("foodman", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.usercollection"))
        body.add_control_add_user()
        for user in User.query.all():
            item = {"username": user.username,
                    "email": user.email}
            body["items"].append(item)
        
        return Response(json.dumps(body), status=200, mimetype=MASON)
    
    def post(self):
        pass

class UserItem(Resource):

    def get(self, username):
        db_user = User.query.filter_by(username=username).first()
        if db_user == None:
            return create_error_response(
                    404, "Not found", "User {} does not exist".format(username)
                    )
        body = UserBuilder(
                    username=db_user.username,
                    email=db_user.email
                    )
        body.add_namespace("foodman", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.useritem", username=username))
        body.add_control("profile", USER_PROFILE)
        body.add_control("collection", url_for("api.usercollection"))
        body.add_control_add_user()
        body.add_control_modify_user(username)
        body.add_control_delete_user(username)

        return Response(json.dumps(body), 200, mimetype=MASON)
    def put(self, username):
        pass
    def delete(self, username):
        pass
