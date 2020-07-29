import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import ShoppingList, ShoppingListFoodItem, User, FoodItem
from foodManager import db
from foodManager.utils.responsebuilder import ResponseBuilder, create_error_response
from foodManager.constants import *


class ShoppingListCollection(Resource):

    def get(self, username):
        body = ResponseBuilder()

        body.add_namespace("foodman", "/foodmanager/link-relations/")
        body.add_control("self", url_for("api.shoppinglistcollection", username=username))
        body.add_control_add_shoppinglist(username, "name")
        body["items"] = []

        foundUser = User.query.filter_by(username=username).first()
        foundLists = ShoppingList.query.join(User).filter(User.username == username).all()

        if foundUser is None:
            return create_error_response(
                404, "Not found",
                "User {} not found".format(username)
            )

        for listItem in foundLists:
            item = ResponseBuilder(
                name=listItem.name
            )
            item.add_control("self", url_for("api.shoppinglistitem", name=listItem.name, username=username))
            item.add_control("profile", "/profiles/shoppinglist")
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")


    def post(self, username):
        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(request.json, ShoppingList.get_schema())
        except ValidationError as error:
            return create_error_response(400, "Invalid JSON document", str(error))

        user = User.query.filter_by(username=username).first()

        shoppinglist = ShoppingList(
            name=request.json["name"],
            owner_id=user.id
        )

        try:
            db.session.add(shoppinglist)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409, "Already exists",
                "Shopping list with the name '{}' already exists.".format(request.json["name"])
            )

        return Response(status=201, headers={
            "Location": url_for("api.shoppinglistitem", username=username, name=request.json["name"])
        })


class ShoppingListItem(Resource):

    def get(self, username, name):
        foundUser = User.query.filter_by(username=username).first()
        if foundUser is None:
            return create_error_response(
                404, "Not found",
                "User {} not found".format(username)
            )

        foundList = ShoppingList.query.join(User).filter(User.username == username, ShoppingList.name == name).first()
        if foundList is None:
            return create_error_response(
                404, "Not found",
                "No shopping list with the name {} was found for user {}".format(name, username)
            )

        body = ResponseBuilder(
            name=foundList.name
        )

        body["items"] = []

        #foundList = ShoppingList.query.join(User).filter(User.username == username, ShoppingList.name == name).first()

        items = (
            FoodItem.query
            .join(ShoppingListFoodItem)
            .join(ShoppingList)
            .join(User)
            .filter(User.username == username, ShoppingList.name == name, ShoppingListFoodItem.shopping_list_id == ShoppingList.id, ShoppingListFoodItem.fooditem_id == FoodItem.id)
            ).all()

        for foodItem in items:
            item = ResponseBuilder(
                name=foodItem.name
            )
            item.add_control("self", url_for("api.shoppinglistfooditems", fooditem=foodItem.name, name=name, username=username))
            item.add_control("profile", "/profiles/shoppinglist")
            body["items"].append(item)

        body.add_namespace("foodman", "/foodmanager/link-relations/")
        body.add_control("self", url_for("api.shoppinglistitem", username=username, name=name))
        body.add_control("collection", url_for("api.shoppinglistcollection", username=username))
        body.add_control_edit_shoppinglist(username, name)
        body.add_control_delete_shoppinglist(username, name)
        body.add_control_add_fooditem(username, name)

        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")

    def put(self, username, name):
        foundList = ShoppingList.query.join(User).filter(User.username == username, ShoppingList.name == name).first()
        if foundList is None:
            return create_error_response(
                404, "Not found",
                "Can't find a list: {}".format(foundList)
            )

        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Request must be JSON"
            )

        try:
            validate(request.json,ShoppingList.get_schema())
        except ValidationError as error:
            return create_error_response(400, "Invalid JSON document", str(error))

        foundList.name = request.json["name"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409, "Already exists",
                "You already have a list {}, pick another one".format(username)
            )

    def delete(self, username, name):
        foundList = ShoppingList.query.join(User).filter(User.username == username, ShoppingList.name == name).first()
        if foundList is None:
            return create_error_response(
                404, "Not found",
                "Can't find a list: {}".format(username)
            )

        db.session.delete(foundUser)
        db.session.commit()

        return Response(status=204)

class ShoppingListFoodItems(Resource):

    ## GET one item of a shopping list
    def get(self, username):
        pass



