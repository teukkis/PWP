from flask import Blueprint
from flask_restful import Api

from foodManager.resources import *
from foodManager.resources.user import UserCollection
from foodManager.resources.shopping_list import ShoppingListCollection, ShoppingListItem
from foodManager.resources.pantry import PantryCollection, PantryItem
from foodManager.resources.fooditem import FoodItemCollection

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

#api.add_resource(Entry, "/")
#api.add_resource(Recipes, "/recipes/")
#api.add_resource(Recipe, "/users/<username>/recipes/")
#api.add_resource(Recipe, "/users/<username>/recipes/<recipe_name>")
api.add_resource(UserCollection, "/users/")
#api.add_resource(User, "/users/<username>")
api.add_resource(ShoppingListCollection, "/users/<username>/shopping_list/")
api.add_resource(ShoppingListItem, "/users/<username>/shopping_list/<list_name>/")
api.add_resource(PantryCollection, "/users/<username>/pantry/")
api.add_resource(PantryItem, "/users/<username>/pantry/<item>")
api.add_resource(FoodItemCollection, "/fooditems/")
