import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from foodManager.models import FoodItem
from foodManager import db
from foodManager.utils.responsebuilder import ResponseBuilder, create_error_response
from foodManager.constants import *

class FoodItemCollection(Resource):

    def get(self):
        body = ResponseBuilder(items=[])
        body.add_namespace("foodman", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.fooditemcollection"))
        body.add_control_create_fooditem()
        ingredients = FoodItem.query.all()
        for ingr in ingredients:
            ingr_item = ResponseBuilder(
                    name=ingr.name,
                    type=ingr.type,
                    id=ingr.id
                    )
            ingr_item.add_control("self", url_for("api.fooditemitem", fooditem=ingr.name))
            ingr_item.add_control("collection", url_for("api.fooditemcollection"))
            body["items"].append(ingr_item)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def post(self):
        if not request.json:
            return create_error_response(
                415,
                "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(request.json, FoodItem.get_schema())
        except ValidationError as error:
            return create_error_response(415, "Invalid JSON document", str(error))

        item = FoodItem(name=request.json["name"])
        try:
            item.type = request.json["type"]
        except KeyError:
            pass
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError as error:
            return create_error_response(
                    409,
                    "Already exists",
                    "Ingredient already exists in the database"
                    )
        return Response(
                status=201,
                headers={"Location": url_for("api.fooditemitem", fooditem=item.name)}
                )


class FoodItemItem(Resource):

    def get(self, fooditem):
        item = FoodItem.query.filter_by(name=fooditem).first()
        if item:
            body = ResponseBuilder(name=item.name, type=item.type)
            body.add_namespace("foodman", LINK_RELATIONS_URL)
            body.add_control("self", url_for("api.fooditemitem", fooditem=item.name))
            body.add_control("collection", url_for("api.fooditemcollection"))

            return Response(json.dumps(body), 200, mimetype=MASON)

        return create_error_response(
                404,
                "Not found",
                "Specified ingredient is not in the database")
