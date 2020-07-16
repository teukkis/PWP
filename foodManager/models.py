"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
"""
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
