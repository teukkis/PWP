import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import User, Pantry, ShoppingList
from foodManager import db
from foodManager.utils.responsebuilder import ResponseBuilder, create_error_response
from foodManager.utils.masonbuilder import MasonBuilder

from foodManager.constants import *

class UserCollection(Resource):

    def get(self):
        body = ResponseBuilder(items=[])
        body.add_namespace("foodman", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.usercollection"))
        body.add_control_add_user()
        for user in User.query.all():
            item = MasonBuilder(
                    username=user.username,
                    email=user.email)
            item.add_control("self", url_for(
                                        "api.useritem",
                                        username=user.username))
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def post(self):
        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(request.json, User.get_schema())
        except ValidationError as error:
            return create_error_response(400, "Invalid JSON document", str(error))

        user = User(
            username=str(request.json["username"]),
            email=str(request.json["email"]),
        )

        try:
            db.session.add(user)
            db.session.commit()
            created_user = User.query.filter_by(username=request.json["username"]).first()
            pantry = Pantry(
                    owner_id=created_user.id,
                    in_use=True
                    )
            shoppinglist = ShoppingList(
                    owner_id=created_user.id,
                    name="Default"
                    )
            db.session.add(pantry)
            db.session.add(shoppinglist)
            db.session.commit()
        except IntegrityError as error:
            return create_error_response(
                409, "Already exists",
                "Username or email is already taken"
            )

        return Response(status=201, headers={
            "Location": url_for("api.useritem", username=request.json["username"])
        })

class UserItem(Resource):

    def get(self, username):
        found_user = User.query.filter_by(username=username).first()
        if found_user is None:
            return create_error_response(
                404, "Not found",
                "No user with the username {} was found".format(username)
            )

        body = ResponseBuilder(
            username=found_user.username,
            email=found_user.email
        )

        body.add_namespace("foodman", "/foodmanager/link-relations/")
        body.add_control("self", url_for("api.useritem", username=username))
        body.add_control("collection", url_for("api.usercollection"))
        body.add_control_edit_user(username)
        body.add_control_delete_user(username)
        body.add_control_all_shoppinglists(username)
        body.add_control_get_pantry(username)

        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def put(self, username):
        found_user = User.query.filter_by(username=username).first()
        if found_user is None:
            return create_error_response(
                404, "Not found",
                "No user with the username {} was found".format(username)
            )

        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Request must be JSON"
            )

        try:
            validate(request.json, User.get_schema())
        except ValidationError as error:
            return create_error_response(400, "Invalid JSON document", str(error))

        new_username = request.json["username"]
        new_email = request.json["email"]
        found_user.username = new_username
        found_user.email = new_email


        try:
            db.session.commit()

        except IntegrityError:
            return create_error_response(
                409, "Already exists",
                ("Username {} (or email {}) is "
                "taken, pick another one".format(new_username, new_email))
            )

        body = ResponseBuilder(
            username=new_username,
            email=new_email
        )

        body.add_namespace("foodman", "/foodmanager/link-relations/")
        body.add_control(
                "self",
                url_for("api.useritem", username=new_username)
                )
        body.add_control("collection", url_for("api.usercollection"))
        body.add_control_edit_user(new_username)
        body.add_control_delete_user(new_username)

        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def delete(self, username):
        found_user = User.query.filter_by(username=username).first()
        if found_user is None:
            return create_error_response(
                404, "Not found",
                "No user with the username {} was found".format(username)
            )

        db.session.delete(found_user)
        db.session.commit()

        return Response(status=204)
