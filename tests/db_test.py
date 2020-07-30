import os
import pytest
import tempfile
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.engine import Engine

from foodManager import create_app, db
from foodManager.models import User, ShoppingList, ShoppingListFoodItem,\
                                FoodItem, Pantry, PantryFoodItem


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
            "TESTING": True
            }
    app = create_app(config)

    with app.app_context():
        db.create_all()

    yield app

    os.close(db_fd)
    os.unlink(db_fname)

def _get_user(number=1):
    return User(
            username="test_user{:02}".format(number),
            email="test_user@test.com")

def _get_shopping_list(owner_id=1):
    return ShoppingList(
            owner_id = owner_id,
            name = "shopping list",
            )

def _get_fooditem(name, type):
    return FoodItem(
            name=name,
            type=type
            )

def _get_shopping_list_item(shopping_list_id, fooditem_id, quantity, unit):
   return ShoppingListFoodItem(
           shopping_list_id=shopping_list_id,
           fooditem_id=fooditem_id,
           quantity=quantity,
           unit=unit
           )

def _get_pantry():
    return Pantry(
            owner_id=1,
            in_use=True)

def _get_pantry_fooditem(fooditem_id):
    return PantryFoodItem(
            pantry_id=1,
            fooditem_id=fooditem_id,
            add_date=datetime.now(),
            deleted=False)
"""
def _get_recipe(name, created_by=1):
    return Recipe(
            created_by=created_by,
            name=name,
            add_date=datetime.now(),
            is_public=False)

def _get_recipe_fooditem(fooditem_id, quantity, unit):
    return RecipeFoodItem(
            recipe_id = 1,
            fooditem_id=fooditem_id,
            quantity=quantity,
            unit=unit
            )

def _get_recipe_step(step_num, description):
    return RecipeStep(
            recipe_id = 1,
            step_num=step_num,
            description=description)
"""



def test_create_instances(app):
    """
    Tests that each an instance of each model can be created
    by filling in all the needed values.
    """
    with app.app_context():
        # Create instance of each model
        user = _get_user()
        shopping_list = _get_shopping_list()
        fooditem1 = _get_fooditem("sausage", "meat")
        fooditem2 = _get_fooditem("cheese", "dairy")
        shopping_list_item1 = _get_shopping_list_item(1, 1, 250.0, "g")
        shopping_list_item2 = _get_shopping_list_item(1, 2, 10.0, "slices")
        shopping_list.items.append(shopping_list_item1)
        shopping_list.items.append(shopping_list_item2)
        user.shopping_lists.append(shopping_list)
        #recipe = _get_recipe("Oven sausage")
        #rec_ingr1 = _get_recipe_fooditem(1, 250.0, "g")
        #rec_ingr2 = _get_recipe_fooditem(2, 10.0, "slices")
        #recipe.fooditems.append(rec_ingr1)
        #recipe.fooditems.append(rec_ingr2)
        #rec_step1 = _get_recipe_step(1, "Make cuts on the sausages and place a\
        #        slice of cheese into each cut")
        #rec_step2 = _get_recipe_step(2, "Bake sausages in 200 degree celsius\
        #        oven for 20 minutes, or until cheese has melten")
        #recipe.steps.append(rec_step1)
        #recipe.steps.append(rec_step2)
        #user.recipes.append(recipe)
        pantry = _get_pantry()
        pantry_item = _get_pantry_fooditem(1)
        pantry.items.append(pantry_item)

        # Add to db
        db.session.add(user)
        db.session.add(fooditem1)
        db.session.add(fooditem2)
        db.session.commit()
        db.session.add(pantry)
        db.session.commit()

        # Check that rows exits
        assert User.query.count() == 1
        assert ShoppingList.query.count() == 1
        assert FoodItem.query.count() == 2
        assert ShoppingListFoodItem.query.count() == 2
        #assert Recipe.query.count() == 1
        #assert RecipeFoodItem.query.count() == 2
        #assert RecipeStep.query.count() == 2
        assert Pantry.query.count() == 1
        assert PantryFoodItem.query.count() == 1

        # Check relationships
        assert shopping_list.items[0] == shopping_list_item1
        assert shopping_list.items[1] == shopping_list_item2
        assert shopping_list_item1.shopping_list == shopping_list
        assert shopping_list_item2.shopping_list == shopping_list

        assert pantry.items[0] == pantry_item
        assert pantry_item.pantry == pantry

        #assert recipe.steps[0] == rec_step1
        #assert recipe.steps[1] == rec_step2
        #assert rec_step1.recipe == recipe
        #assert rec_step2.recipe == recipe
        #assert recipe.fooditems[0] == rec_ingr1
        #assert recipe.fooditems[1] == rec_ingr2
        #assert rec_ingr1.recipe == recipe
        #assert rec_ingr2.recipe == recipe

def test_delete_user(app):
    # user is deleted, users shopping list is also deleted
    with app.app_context():
        user = _get_user()
        shopping_list = _get_shopping_list()
        pantry = _get_pantry()
        user.shopping_lists.append(shopping_list)
        db.session.add(user)
        db.session.commit()
        db.session.add(pantry)
        db.session.commit()

        # shopping list, pantry exist and belong to user
        shopping_lists = ShoppingList.query.all()
        pantries = Pantry.query.all()
        assert len(shopping_lists) == 1
        assert len(pantries) == 1
        assert user.id == 1
        assert shopping_list.owner_id == 1
        assert pantry.owner_id == 1

        # shopping list and pantry don't exists after deleting user
        db.session.delete(user)
        db.session.commit()
        shopping_lists = ShoppingList.query.all()
        pantries = Pantry.query.all()
        assert len(shopping_lists) == 0
        assert len(pantries) == 0

def test_delete_shopping_list(app):
    # delete shopping list items and shopping lists
    with app.app_context():
        user = _get_user()
        shopping_list = _get_shopping_list()
        fooditem = _get_fooditem("bratwurst", "meat")
        db.session.add(user)
        db.session.add(fooditem)
        db.session.commit()

        shopping_list_item = _get_shopping_list_item(1, 1, 200.0, "g")
        shopping_list.items.append(shopping_list_item)
        user.shopping_lists.append(shopping_list)
        db.session.commit()

        # user, shopping list and shopping list item exist
        shopping_lists = ShoppingList.query.all()
        shopping_list_items = ShoppingListFoodItem.query.all()
        assert len(shopping_lists) == 1
        assert len(user.shopping_lists) == 1
        assert len(shopping_list_items) == 1
        assert user.shopping_lists[0].id == shopping_lists[0].id

        # test that shopping list item and users shopping list relation is also deleted
        db.session.delete(shopping_list)
        db.session.commit()
        shopping_list_items = ShoppingListFoodItem.query.all()
        assert len(user.shopping_lists) == 0
        assert len(shopping_list_items) == 0

def test_delete_pantry(app):
    # delete pantry -> pantry fooditems are deleted also
    with app.app_context():
        user = _get_user()
        fooditem = _get_fooditem("nikka from the barrel", "beverage")
        db.session.add(user)
        db.session.add(fooditem)
        db.session.commit()

        pantry = _get_pantry()
        db.session.add(pantry)
        db.session.commit()

        pantryfooditem = _get_pantry_fooditem(fooditem.id)
        db.session.add(pantryfooditem)
        db.session.commit()

        # pantry and pantryfooditem exist, and ids match
        pantries = Pantry.query.all()
        pantryfooditems = PantryFoodItem.query.all()
        assert len(pantries) == 1
        assert len(pantryfooditems) == 1
        assert pantryfooditem.pantry_id == pantry.id

        # pantry fooditems get deleted as pantry gets deleted
        db.session.delete(pantry)
        db.session.commit()
        pantries = Pantry.query.all()
        pantryfooditems = PantryFoodItem.query.all()
        assert len(pantryfooditems) == 0
        assert len(pantries) == 0

def test_user_columns(app):
    # username and email must be unique
    with app.app_context():
        user = _get_user()
        user2 = _get_user() # same username
        user2.email = "tester2@test.com"
        db.session.add(user)
        db.session.add(user2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        user2.email = "test_user@test.com" # same email
        user2.username = "testerboi"
        db.session.add(user)
        db.session.add(user2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # username is not nullable
        user.username = None
        db.session.add(user)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        # email is not nullable
        user2.email = None
        db.session.add(user2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()
