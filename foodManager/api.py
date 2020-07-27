import json
from flask import Response, Blueprint, url_for
from flask_restful import Api

from foodManager.resources import *
from foodManager.constants import *

from foodManager.resources.user import UserCollection, UserItem
from foodManager.resources.shopping_list import ShoppingListCollection, ShoppingListItem, ShoppingListFoodItems
from foodManager.resources.pantry import PantryCollection, PantryFoodItem
from foodManager.resources.fooditem import FoodItemCollection, FoodItemItem
from foodManager.utils.responsebuilder import ResponseBuilder

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

#api.add_resource(Recipes, "/recipes/")
#api.add_resource(Recipe, "/users/<username>/recipes/")
#api.add_resource(Recipe, "/users/<username>/recipes/<recipe_name>")
api.add_resource(UserCollection, "/users/")
api.add_resource(UserItem, "/users/<username>")
api.add_resource(ShoppingListCollection, "/users/<username>/shoppinglists/")
api.add_resource(ShoppingListItem, "/users/<username>/shoppinglists/<name>")
api.add_resource(ShoppingListFoodItems, "/users/<username>/shoppinglists/<name>/<fooditem>")
api.add_resource(PantryCollection, "/users/<username>/pantry/")
api.add_resource(PantryFoodItem, "/users/<username>/pantry/<fooditem>")
api.add_resource(FoodItemCollection, "/fooditems/")
api.add_resource(FoodItemItem, "/fooditems/<fooditem>")

@api_bp.route("/")
def entry():
    body = ResponseBuilder()
    body.add_namespace("foodman", LINK_RELATIONS_URL)
    body.add_control(
            "foodman:users-all",
            url_for("api.usercollection"),
            )
    body.add_control(
            "foodman:fooditems-all",
            url_for("api.fooditemcollection"),
            )
    return Response(json.dumps(body), 200, mimetype=MASON)
