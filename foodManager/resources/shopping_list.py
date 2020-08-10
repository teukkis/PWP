import json
import sys
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
        body.add_control_add_shoppinglist(username)
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
            item.add_control("collection", url_for("api.shoppinglistcollection", username=username))
            item.add_control("profile", "/profiles/shoppinglist")
            item.add_control_add_fooditem(username, listItem.name)
            item.add_control_edit_shoppinglist(username, listItem.name)
            item.add_control_delete_shoppinglist(username, listItem.name)
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
        # model allows same shopping list name for multiple shopping lists
        # but resource URL is based on the name being unique..
        # dirty fix:
        sls = ShoppingList.query.filter_by(owner_id=user.id).all()
        for sl in sls:
            if sl.name == request.json["name"]:
                return create_error_response(
                        409, "Already exists",
                        "Shopping list with the name '{}' already exists.".format(request.json["name"]))

        db.session.add(shoppinglist)
        db.session.commit()

        """
        try:
            db.session.add(shoppinglist)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409, "Already exists",
                "Shopping list with the name '{}' already exists.".format(request.json["name"])
            )
        """

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
            name=foundList.name,
            id=foundList.id
        )

        body["items"] = []

        items = (
            db.session.query(ShoppingListFoodItem, FoodItem)
            .join(FoodItem)
            .join(ShoppingList)
            .join(User)
            .filter(User.username == username, ShoppingList.name == name, ShoppingListFoodItem.shopping_list_id == ShoppingList.id, ShoppingListFoodItem.fooditem_id == FoodItem.id)
            ).all()

        for shoppingListFoodItem, foodItem in items:
            print(foodItem)
            item = ResponseBuilder(
                name=foodItem.name,
                quantity=shoppingListFoodItem.quantity,
                unit=shoppingListFoodItem.unit,
                shopping_list_id=shoppingListFoodItem.shopping_list_id,
                fooditem_id=shoppingListFoodItem.fooditem_id
            )
            item.add_control("self", url_for("api.shoppinglistfooditems", fooditem=foodItem.name, name=name, username=username))
            item.add_control("profile", "/profiles/shoppinglist")
            item.add_control_delete_shopping_list_item(username, name, foodItem.name)
            item.add_control_edit_shopping_list_food_item(username, name, foodItem.name)
            body["items"].append(item)

        body.add_namespace("foodman", "/foodmanager/link-relations/")
        body.add_control("self", url_for("api.shoppinglistitem", username=username, name=name))
        body.add_control("collection", url_for("api.shoppinglistcollection", username=username))
        body.add_control_edit_shoppinglist(username, name)
        body.add_control_delete_shoppinglist(username, name)
        body.add_control_add_fooditem(username, name)
        body.add_control_get_all_fooditems()

        return Response(json.dumps(body), 200, mimetype="application/vnd.mason+json")



    def post(self, username, name):
        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(request.json, ShoppingListFoodItem.get_schema())
        except ValidationError as error:
            return create_error_response(400, "Invalid JSON document", str(error))


        foundList = ShoppingList.query.join(User).filter(User.username == username, ShoppingList.name == name).first()

        newShoppinglistFoodItem = ShoppingListFoodItem(
            shopping_list_id=request.json["shopping_list_id"],
            fooditem_id=request.json["fooditem_id"],
        )



        try:
            db.session.add(newShoppinglistFoodItem)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409, "Already exists",
                "Food item with the name '{}' already exists.".format(request.json["name"])
            )

        return Response(status=201)




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
                "You already have a list {}, pick another one".format(name)
            )

    def delete(self, username, name):
        foundList = ShoppingList.query.join(User).filter(User.username == username, ShoppingList.name == name).first()
        if foundList is None:
            return create_error_response(
                404, "Not found",
                "Can't find a list: {}".format(username)
            )

        db.session.delete(foundList)
        db.session.commit()

        return Response(status=204)

class ShoppingListFoodItems(Resource):

    ## DELETE one shopping list item
    def delete(self, username, name, fooditem):
        foundItem = (
            ShoppingListFoodItem.query
            .join(FoodItem)
            .join(ShoppingList)
            .join(User)
            .filter(User.username == username, ShoppingList.name == name, ShoppingListFoodItem.shopping_list_id == ShoppingList.id, ShoppingListFoodItem.fooditem_id == FoodItem.id, FoodItem.name == fooditem)
            ).first()

        if foundItem is None:
            return create_error_response(
                404, "Not found",
                "Can't find an item: {}".format(fooditem)
            )

        db.session.delete(foundItem)
        db.session.commit()

        return Response(status=204)

    def put(self, username, name, fooditem):
        foundItem = (
            ShoppingListFoodItem.query
            .join(FoodItem)
            .join(ShoppingList)
            .join(User)
            .filter(User.username == username, ShoppingList.name == name, ShoppingListFoodItem.shopping_list_id == ShoppingList.id, ShoppingListFoodItem.fooditem_id == FoodItem.id, FoodItem.name == fooditem)
            ).first()

        if foundItem is None:
            return create_error_response(
                404, "Not found",
                "Can't find an item: {}".format(fooditem)
            )

        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Request must be JSON"
            )

        try:
            validate(request.json, ShoppingListFoodItem.get_schema())
        except ValidationError as error:
            return create_error_response(400, "Invalid JSON document", str(error))


        foundItem.quantity=request.json["quantity"]
        shopping_list_id=request.json["shopping_list_id"],
        fooditem_id=request.json["fooditem_id"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409, "Already exists",
                "You already have {} on the list: {}".format(fooditem, name)
            )

