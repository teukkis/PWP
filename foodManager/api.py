from flask import Flask
from flask_resrful import Resource, Api

from food_manager.resources.recipe import Recipes, Recipe
from food_manager.resources.user import Users, User
from food_manager.resources.shopping_list import Shopping_lists, Shopping_list
from food_manager.resources.shopping_list import Pantry, PantryItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(Entry, "/")
api.add_resource(Recipes, "/recipes/")
api.add_resource(Recipe, "/<username>/recipes/")
api.add_resource(Recipe, "/<username>/recipes/<recipe_name>")
api.add_resource(Users, "/users/")
api.add_resource(User, "/users/<username>")
api.add_resource(Shopping_lists, "/<username>/shopping_list/")
api.add_resource(Shopping_list, "/<username>/shopping_list/<list_name/")
api.add_resource(Pantry, "/<username>/pantry/")
api.add_resource(PantryItems, "/<username>/pantry/<items>")

