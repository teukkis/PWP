from flask import Blueprint
from flask_restful import Api

from foodManager.resources import *
from foodManager.resources.user import Users, User
from foodManager.resources.shopping_list import ShoppingListCollection, ShoppingList
from foodManager.resources.pantry import Pantry, PantryItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

#api.add_resource(Entry, "/")
#api.add_resource(Recipes, "/recipes/")
#api.add_resource(Recipe, "/users/<username>/recipes/")
#api.add_resource(Recipe, "/users/<username>/recipes/<recipe_name>")
api.add_resource(Users, "/users/")
api.add_resource(User, "/users/<username>")
api.add_resource(ShoppingListCollection, "/users/<username>/shopping_list/")
api.add_resource(ShoppingList, "/users/<username>/shopping_list/<list_name>/")
api.add_resource(Pantry, "/users/<username>/pantry/")
api.add_resource(PantryItem, "/users/<username>/pantry/<item>")

@api_bp.route("/")
def index():
    return "asd1", 200
