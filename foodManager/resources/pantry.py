import json
from datetime import datetime
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import Pantry, PantryFoodItem, FoodItem, User
from foodManager import db
from foodManager.utils.responsebuilder import ResponseBuilder, create_error_response
from foodManager.constants import *

class PantryCollection(Resource):

    def get(self, username):
        db_user = User.query.filter_by(username=username).first()
        if not db_user:
            return create_error_response(
                    404,
                    "Not found",
                    "User {} not found".format(username)
                    )
        db_pantry = Pantry.query.filter_by(owner_id=db_user.id).first()
        if not db_pantry:
            return create_error_response(
                    404,
                    "Not found",
                    "Pantry for user {} not found".format(username)
                    )
        body = ResponseBuilder(items=[])
        body.add_namespace("foodman", LINK_RELATIONS_URL)
        db_pantryfooditems = PantryFoodItem.query.filter_by(pantry_id=db_pantry.id).all()
        for item in db_pantryfooditems:
            if item.deleted == False:
                db_fooditem = FoodItem.query.filter_by(id=item.fooditem_id).first()
                body["items"].append(
                        {
                            "name": db_fooditem.name,
                            "fooditem_id": db_fooditem.id,
                            "add_date": item.add_date,
                            "href": url_for("api.pantryfooditemitem",
                                username=username, fooditem=db_fooditem.name)
                        }
                        )
        body.add_control("self", url_for("api.pantrycollection",
                                        username=username))
        body.add_control_add_pantry_fooditem(username)
        return Response(json.dumps(body, default=str), 200, mimetype=MASON)

    def post(self, username):
        if not request.json:
            return create_error_response(
                    415,
                    "Unsupported media type",
                    "Request must be JSON"
                    )
        try:
            validate(request.json, PantryFoodItem.get_schema())
        except ValidationError as error:
            return create_error_response(400, "Invalid JSON document", str(error))

        db_user = User.query.filter_by(username=username).first()
        if not db_user:
            return create_error_response(
                    404,
                    "Not found",
                    "User {} not found".format(username)
                    )

        db_pantry = Pantry.query.filter_by(owner_id=db_user.id).first()
        if not db_pantry:
            return create_error_response(
                    404,
                    "Not found",
                    "Pantry for user {} not found".format(username)
                    )
        pantry_fooditem = PantryFoodItem(
                            pantry_id=db_pantry.id,
                            fooditem_id=request.json["fooditem_id"],
                            add_date=datetime.now(),
                            deleted=False
                            )
        try:
            db.session.add(pantry_fooditem)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                    409,
                    "Already exists",
                    "Ingredient is already in the pantry")
        db_fooditem = FoodItem.query.filter_by(id=request.json["fooditem_id"]).first()
        return Response(201, headers={"Location":
                            url_for("api.pantryfooditemitem",
                                username=username,
                                fooditem=db_fooditem.name)})

class PantryFoodItemItem(Resource):

    def get(self, username, fooditem):
        db_user = User.query.filter_by(username=username).first()
        if not db_user:
            return create_error_response(
                    404,
                    "Not found",
                    "User {} not found".format(username)
                    )
        db_pantry = Pantry.query.filter_by(owner_id=db_user.id).first()
        if not db_pantry:
            return create_error_response(
                    404,
                    "Not found",
                    "Pantry for user {} not found".format(username)
                    )
        db_fooditem = FoodItem.query.filter_by(name=fooditem).first()
        if not db_fooditem:
            return create_error_response(
                    404,
                    "Not found",
                    "Fooditem {} for pantry of user {} not found".format(
                                                        fooditem,username)
                    )
        db_pantryfooditem = PantryFoodItem.query.filter_by(
                                                    pantry_id=db_pantry.id,
                                                    fooditem_id=db_fooditem.id
                                                    ).first()
        body = ResponseBuilder()
        body.add_namespace("foodman", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.pantryfooditemitem",
                                        username=username, fooditem=fooditem))
        body.add_control_delete_pantry_fooditem(username, fooditem)
        return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, item):
        pass

    def delete(self, username, fooditem):
        db_user = User.query.filter_by(username=username).first()
        if not db_user:
            return create_error_response(
                    404,
                    "Not found",
                    "User {} not found".format(username)
                    )

        db_pantry = Pantry.query.filter_by(owner_id=db_user.id).first()
        if not db_pantry:
            return create_error_response(
                    404,
                    "Not found",
                    "Pantry for user {} not found".format(username)
                    )
        db_fooditem = FoodItem.query.filter_by(name=fooditem).first()
        if not db_fooditem:
            return create_error_response(
                    404,
                    "Not found",
                    "Ingredient {} not found".format(fooditem)
                    )
        db_pantry_fooditem = PantryFoodItem.query.filter_by(
                                                pantry_id=db_pantry.id,
                                                fooditem_id=db_fooditem.id
                                                ).first()
        if not db_pantry_fooditem:
            return create_error_response(
                    404,
                    "Not found",
                    "Fooditem {} for pantry of user {} not found".format(
                                                        fooditem,username)
                    )
        db.session.delete(db_pantry_fooditem)
        db.session.commit()
        return Response(status=204)
