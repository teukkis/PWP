import json
from flask import Response, request, url_for
from foodManager.constants import *
from foodManager.models import *
from foodManager.utils.masonbuilder import MasonBuilder



class ResponseBuilder(MasonBuilder):

    #Controls for users
    def add_control_delete_user(self, username):
        self.add_control(
            "delete",
            url_for("api.useritem", username=username),
            method="DELETE",
            title="Delete this user"
        )

    def add_control_add_user(self):
        self.add_control(
            "foodman:add-user",
            url_for("api.usercollection"),
            method="POST",
            encoding="json",
            title="Create a new user",
            schema=User.get_schema()
        )

    def add_control_edit_user(self, username):
        self.add_control(
            "edit",
            url_for("api.useritem", username=username),
            method="PUT",
            title="edit this user",
            encoding="json",
            schema=User.get_schema()
        )


    #Controls for shopping lists
    def add_control_add_shoppinglist(self, username):
        self.add_control(
            "foodman:add-shoppinglist",
            url_for("api.shoppinglistcollection", username=username),
            method="POST",
            encoding="json",
            title="Create a new shopping list",
            schema=ShoppingList.get_schema()
        )

    def add_control_edit_shoppinglist(self, username, name):
        self.add_control(
            "edit",
            url_for("api.shoppinglistitem", username=username, name=name),
            method="PUT",
            title="edit shopping list name",
            encoding="json",
            schema=ShoppingList.get_schema()
        )

    def add_control_delete_shoppinglist(self, username, name):
        self.add_control(
            "delete",
            url_for("api.shoppinglistitem", username=username, name=name),
            method="DELETE",
            title="Delete shopping list"
        )

    def add_control_delete_shopping_list_item(self, username, name, fooditem):
        self.add_control(
            "foodman:delete",
            url_for("api.shoppinglistfooditems", username=username, name=name, fooditem=fooditem),
            method="DELETE",
            title="Delete shopping list food item"
        )

    def add_control_add_fooditem(self, username, sl_name):
        self.add_control(
            "foodman:add-fooditem",
            url_for("api.shoppinglistitem", username=username, name=sl_name),
            method="POST",
            encoding="json",
            title="Add ingredient to the shopping list",
            schema=ShoppingListFoodItem.get_schema()
        )

    def add_control_all_shoppinglists(self, username):
        self.add_control(
            "foodman:all-shoppinglists",
            url_for("api.shoppinglistcollection", username=username),
            method="GET",
        )

    def add_control_edit_shopping_list_food_item(self, username, name, fooditem):
        self.add_control(
            "foodman:edit-shoppinglistitems",
            url_for("api.shoppinglistfooditems", username=username, name=name, fooditem=fooditem),
            method="PUT",
        )

    #Controls for food item
    def add_control_create_fooditem(self):
        self.add_control(
            "foodman:create-fooditem",
            url_for("api.fooditemcollection"),
            method="POST",
            encoding="json",
            title="Add an ingredient to the database",
            schema=FoodItem.get_schema()
        )

    #Pantry
    def add_control_get_pantry(self, username):
        self.add_control(
            "foodman:get-pantry",
            url_for("api.pantrycollection", username=username),
            method="GET",
        )

    #foodItem storage
    def add_control_get_all_fooditems(self):
        self.add_control(
            "foodman:all-fooditems",
            url_for("api.fooditemcollection"),
            method="GET",
        )

    def add_control_add_pantry_fooditem(self, username):
        self.add_control(
            "foodman:add-pantry-fooditem",
            url_for("api.pantrycollection", username=username),
            method="POST",
            encoding="json",
            title="Add ingredient to pantry",
            schema=PantryFoodItem.get_schema()
        )

    def add_control_delete_pantry_fooditem(self, username, fooditem):
        self.add_control(
            "delete",
            url_for("api.pantryfooditemitem",
                    username=username, fooditem=fooditem),
            method="DELETE",
            title="Delete ingredient from pantry",
        )

    @staticmethod
    def _paginator_schema():
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        props = schema["properties"]
        props["index"] = {
            "description": "Starting index for pagination",
            "type": "integer",
            "default": "0"
        }
        return schema

def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href="/profiles/error/")
    return Response(json.dumps(body), status_code, mimetype="application/vnd.mason+json")
