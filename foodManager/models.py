import click
from flask.cli import with_appcontext
from foodManager import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)

    shopping_lists = db.relationship("ShoppingList", cascade="all, delete-orphan", back_populates="owner")
    #recipes = db.relationship("Recipe", back_populates="creator")

    def __repr__(self):
        return "{} <{}>".format(self.username, self.id)
    
    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["username", "email"]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "description": "Unique username for the user",
            "type": "string"
        }
        props["email"] = {
            "description": "Unique email for the user",
            "type": "string"
        }
        return schema

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    name = db.Column(db.String(64), unique=False, nullable=False)

    owner = db.relationship("User", back_populates="shopping_lists")
    items = db.relationship("ShoppingListFoodItem", cascade="all, delete-orphan", back_populates="shopping_list")


class ShoppingListFoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey("shopping_list.id", ondelete="CASCADE"))
    fooditem_id = db.Column(db.Integer, db.ForeignKey("food_item.id"))
    quantity = db.Column(db.Float, unique=False, nullable=True)
    unit = db.Column(db.String(16), unique=False, nullable=True)

    shopping_list = db.relationship("ShoppingList", back_populates="items")


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    type = db.Column(db.String(64), unique=False, nullable=True)

    #def __repr__(self):
    #    return "{} ({}) <{}>".format(self.name, self.type, self.id)

class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    in_use = db.Column(db.Boolean, unique=False, nullable=False)

    items = db.relationship("PantryFoodItem", back_populates="pantry")

class PantryFoodItem(db.Model):
    pantry_id = db.Column(db.Integer, db.ForeignKey("pantry.id"), primary_key=True)
    fooditem_id = db.Column(db.Integer, db.ForeignKey("food_item.id"), primary_key=True)
    add_date = db.Column(db.DateTime, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False)

    pantry = db.relationship("Pantry", back_populates="items")

@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()

@click.command("testgen")
@with_appcontext
def generate_test_data():
    # create test users
    for i in range(1,7):
        user = User(
                username="test_user{:02}".format(i),
                email="test_user{:02}@test.com".format(i))
        db.session.add(user)
    db.session.commit()

    # create fooditems
    with open('foodManager/utils/db_init_txt/fooditems.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            splitted_lines = line.split(',')
            _type = splitted_lines.pop(0)
            last = splitted_lines.pop(-1)
            ingr = FoodItem(name=last[:-1], type=_type)
            db.session.add(ingr)
            for name in splitted_lines:
                ingr = FoodItem(name=name, type=_type)
                db.session.add(ingr)
        db.session.commit()


    # create shoppinglists, (and pantries)
    for user in User.query.all():
        sl = ShoppingList(owner_id=user.id, name="Personal")
        in_use = user.id%3==0
        pantry = Pantry(owner_id=user.id, in_use=in_use)
        db.session.add(sl)
        db.session.add(pantry)
        db.session.commit()
        user.shopping_lists.append(sl)
    # create shopping list items
    with open('foodManager/utils/db_init_txt/shoppinglists.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            splitted = line.split(',')
            sl_id = splitted.pop(0)
            ingr_id = splitted.pop(0)
            qty = splitted.pop(0)
            unit = splitted.pop(0)
            sli = ShoppingListFoodItem()
            sli.shopping_list_id = sl_id
            sli.fooditem_id = ingr_id
            if qty != "":
                sl.quantity = qty
            if unit != "":
                sl.unit = unit
            sl = ShoppingList.query.filter_by(id=sl_id).first()
            sl.items.append(sli)
            db.session.commit()
    # create pantry items
    with open('foodManager/utils/db_init_txt/pantries.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            splitted = line.split(',')
            pantry_id = splitted.pop(0)
            ingr_id = splitted.pop(0)
            add_date = datetime.now()
            deleted = splitted.pop(0)[:-1] # remove newline             
            if deleted == 'false':
                deleted = False
            elif deleted == 'true':
                deleted = True
            pantry_item = PantryFoodItem(
                                        pantry_id=pantry_id,
                                        fooditem_id=ingr_id,
                                        add_date=add_date,
                                        deleted=deleted
                                            )
            pantry = Pantry.query.filter_by(id=pantry_id).first()
            pantry.items.append(pantry_item)
            db.session.commit()

# these are currently not implemented
"""
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id",
                            ondelete="SET NULL"), nullable=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    add_date = db.Column(db.DateTime, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)

    creator = db.relationship("User", back_populates="recipes")
    steps = db.relationship("RecipeStep", back_populates="recipe")
    fooditems = db.relationship("RecipeFoodItem",
                                         back_populates="recipe")


class RecipeStep(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))
    step_num = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), unique=False, nullable=False)

    recipe = db.relationship("Recipe", back_populates="steps")


class RecipeFoodItem(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    fooditem_id = db.Column(db.Integer, db.ForeignKey("food_item.id"), primary_key=True)
    quantity = db.Column(db.Float, unique=False, nullable=True)
    unit = db.Column(db.String(16), unique=False, nullable=True)

    recipe = db.relationship("Recipe", back_populates="fooditems")
"""
