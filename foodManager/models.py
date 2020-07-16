import click
from flask.cli import with_appcontext
from foodManager import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)

    shopping_lists = db.relationship("ShoppingList", cascade="all, delete-orphan", back_populates="owner")
    #recipes = db.relationship("Recipe", back_populates="creator")

    def __repr__(self):
        return "{} <{}>".format(self.username, self.id)

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    name = db.Column(db.String(64), unique=False, nullable=False)

    owner = db.relationship("User", back_populates="shopping_lists")
    items = db.relationship("ShoppingListItem", cascade="all, delete-orphan", back_populates="shopping_list")


class ShoppingListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey("shopping_list.id", ondelete="CASCADE"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"))
    quantity = db.Column(db.Float, unique=False, nullable=True)
    unit = db.Column(db.String(16), unique=False, nullable=True)

    shopping_list = db.relationship("ShoppingList", back_populates="items")


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    type = db.Column(db.String(64), unique=False, nullable=True)

    def __repr__(self):
        return "{} ({}) <{}>".format(self.name, self.type, self.id)

class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    in_use = db.Column(db.Boolean, unique=False, nullable=False)

    items = db.relationship("PantryItem", back_populates="pantry")

class PantryItem(db.Model):
    pantry_id = db.Column(db.Integer, db.ForeignKey("pantry.id"), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)
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
    for i in range(1,6):
        user = User(
                username="test_user{:02}".format(i),
                email="test_user{:02}@test.com".format(i))
        db.session.add(user)
    db.session.commit()

    # create ingredients
    with open('foodManager/utils/db_init_txt/ingredients.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            splitted_lines = line.split(',')
            _type = splitted_lines.pop(0)
            for name in splitted_lines:
                ingr = Ingredient(name=name, type=_type)
                db.session.add(ingr)
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
    ingredients = db.relationship("RecipeIngredient",
                                         back_populates="recipe")


class RecipeStep(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))
    step_num = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), unique=False, nullable=False)

    recipe = db.relationship("Recipe", back_populates="steps")


class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)
    quantity = db.Column(db.Float, unique=False, nullable=True)
    unit = db.Column(db.String(16), unique=False, nullable=True)

    recipe = db.relationship("Recipe", back_populates="ingredients")
"""
