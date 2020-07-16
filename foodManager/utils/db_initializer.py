from app import db
from app import User, ShoppingList, ShoppingListItem, Ingredient, Pantry,\
                PantryItem, Recipe, RecipeStep, RecipeIngredient
from os import path, remove

def _get_user(number=1):
    return User(
            username="test_user{:02}".format(number),
            email="test_user{:02}@test.com".format(number))

def _get_shopping_list(owner_id=1):
    return ShoppingList(
            owner_id = owner_id,
            name = "shopping list",
            )

def _get_ingredient(name, type):
    return Ingredient(
            name=name,
            type=type
            )

def _get_shopping_list_item(shopping_list_id, ingredient_id, quantity, unit):
   return ShoppingListItem(
           shopping_list_id=shopping_list_id,
           ingredient_id=ingredient_id,
           quantity=quantity,
           unit=unit
           )

def _get_recipe(name, created_by=1):
    return Recipe(
            created_by=created_by,
            name=name,
            add_date=datetime.now(),
            is_public=False)

def _get_recipe_ingredient(ingredient_id, quantity, unit):
    return RecipeIngredient(
            recipe_id = 1,
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
            )

def _get_recipe_step(step_num, description):
    return RecipeStep(
            recipe_id = 1,
            step_num=step_num,
            description=description)


def _get_pantry():
    return Pantry(
            owner_id=1,
            in_use=True)

def _get_pantry_item(ingredient_id):
    return PantryItem(
            pantry_id=1,
            ingredient_id=ingredient_id,
            add_date=datetime.now(),
            deleted=False)

def main():
    # prompt user if db already exists
    if path.exists("test.db"):
        print("test.db already exists, do you want to initialize the database? (y/n)")
        answer = input(">")
        if answer.lower() == "n":
            exit()
        else:
            remove("test.db")
    # create db
    db.create_all()

    # create users
    for i in range(1,6):
        user = _get_user(i)
        db.session.add(user)
    db.session.commit()
    print(User.query.all())

    # create ingredients
    with open('db_initialization/ingredients.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            splitted_lines = line.split(',')
            _type = splitted_lines.pop(0)
            for name in splitted_lines:
                ingr = Ingredient(name=name, type=_type)
                db.session.add(ingr)
        db.session.commit()
    for ing in Ingredient.query.all():
        print(ing)

if __name__ == "__main__":
    main()
