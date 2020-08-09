import json
import os
import pytest
import tempfile
import time
from datetime import datetime

from jsonschema import validate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, StatementError

from foodManager import create_app, db
from foodManager.models import User, ShoppingList, ShoppingListFoodItem,\
                                FoodItem, Pantry, PantryFoodItem


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
            "TESTING": True
            }

    app = create_app(config)

    with app.app_context():
        db.create_all()
        _generate_db_data()

    yield app.test_client()

    os.close(db_fd)
    os.unlink(db_fname)

def _generate_db_data():
    # create three users
    for i in range(1, 4):
        user = User(
                username="test_user{}".format(i),
                email="test{}@test.com".format(i)
                )
        db.session.add(user)
    db.session.commit()

    # create pantry and shopping list for users
    users = User.query.all()
    for user in users:
        pantry = Pantry(
                owner_id=user.id,
                in_use=True
                )
        shopping_list = ShoppingList(
                        owner_id=user.id,
                        name="personal"
                        )
        user.shopping_lists.append(shopping_list)
        db.session.add(pantry)
    db.session.commit()

    # create fooditems
    foods = [
            ("redbull", "beverage"),
            ("asahi", "beverage"),
            ("glenlivet", "beverage")
            ]
    for n, t in foods:
        food = FoodItem(
                name=n,
                type=t
                )
        db.session.add(food)
    db.session.commit()

    foods = FoodItem.query.all()
    pantry = Pantry.query.filter_by(owner_id=1).first()
    pantryfooditem = PantryFoodItem(
                        pantry_id=pantry.id,
                        fooditem_id=foods[0].id,
                        add_date=datetime.now(),
                        deleted=False
                        )
    sl = ShoppingList.query.filter_by(owner_id=1).first()
    slfooditem = ShoppingListFoodItem(
                    shopping_list_id=sl.id,
                    fooditem_id=foods[2].id,
                    quantity=1,
                    unit="bottles"
                )
    db.session.add(pantryfooditem)
    db.session.add(slfooditem)
    db.session.commit()

# following helper functions heavily inspired by
# https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py

def _check_namespace(client, response):
    """
    Test that "foodman" namespace is found in the response and
    and the href value can be used to get a valid response.
    """
    namespace_href = response["@namespaces"]["foodman"]["name"]
    resp = client.get(namespace_href)
    assert resp.status_code == 200

def _check_control_get(ctrl, client, obj):
    """
    Tests the existence of a control that uses GET method
    and also that the href of the control works.
    """
    href = obj["@controls"][ctrl]["href"]
    print(href)
    resp = client.get(href)
    assert resp.status_code == 200

def _check_control_post(ctrl, client, obj, json_func):
    """
    Validates the href, method, encoding and schema for POST.
    """
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = json_func()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_put(ctrl, client, obj, json_func):
    """
    """

    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = json_func()
    body["username"] = obj["username"]
    body["email"] = obj["email"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 200

def _check_control_delete(ctrl, client, obj):
    """
    """

    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204

def _get_user_json(username="dummy_user", email="dummy@user.com"):
    """
    Creates a dummy user json to be used in tests.
    """
    return {"username": username, "email": email}


class TestUserCollection(object):
    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)
        _check_control_post("foodman:add-user",
                            client,
                            resp_body,
                            _get_user_json)
        assert len(resp_body["items"]) == 3
        for item in resp_body["items"]:
            assert "username" in item
            assert "email" in item
            _check_control_get("self", client, item)

    def test_post(self, client):
        user_json = _get_user_json()

        # invalid content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(user_json))
        assert resp.status_code == 415

        # valid post
        resp = client.post(self.RESOURCE_URL, json=user_json)
        assert resp.status_code == 201

        # location header looks correct
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + user_json["username"])

        # location headers url works
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200

        # duplicate data
        resp = client.post(self.RESOURCE_URL, json=user_json)
        assert resp.status_code == 409

        # missing data
        user_json.pop("email")
        resp = client.post(self.RESOURCE_URL, json=user_json)
        assert resp.status_code == 400

class TestUserItem(object):
    RESOURCE_URL1 = "/api/users/test_user1"
    RESOURCE_URL2 = "/api/users/test_user2"
    INVALID_URL = "/api/users/nobody"

    def test_get(self, client):
        # test valid get
        response = client.get(self.RESOURCE_URL1)
        assert response.status_code == 200
        resp_body = json.loads(response.data)

        # test namespace and controls
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)
        _check_control_get("collection", client, resp_body)
        _check_control_put("edit", client, resp_body, _get_user_json)
        _check_control_delete("delete", client, resp_body)

        # test invalid invalid url
        response = client.get(self.INVALID_URL)
        assert response.status_code == 404

    def test_put(self, client):
        # change username
        user = _get_user_json("herbert", "test1@test.com")

        # invalid content type
        response = client.put(self.RESOURCE_URL1, data=json.dumps(user))
        assert response.status_code == 415

        # valid put
        response = client.put(self.RESOURCE_URL1, json=user)
        assert response.status_code == 200
        resp_body = json.loads(response.data)

        # test namespace and controls
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)
        _check_control_get("collection", client, resp_body)
        _check_control_put("edit", client, resp_body, _get_user_json)
        _check_control_delete("delete", client, resp_body)

        # user not found
        response = client.put(self.INVALID_URL, json=user)
        assert response.status_code == 404

        # username already exists
        user["username"] = "test_user3"
        user["email"] = "test2@test.com"
        response = client.put(self.RESOURCE_URL2, json=user)
        assert response.status_code == 409

        # email already exists
        user["username"] = "test_user2"
        user["email"] = "test3@test.com"
        response = client.put(self.RESOURCE_URL2, json=user)
        assert response.status_code == 409


    def test_delete(self, client):
        # valid delete
        response = client.delete(self.RESOURCE_URL1)
        assert response.status_code == 204

        # try to delete same user again
        response = client.delete(self.RESOURCE_URL1)
        assert response.status_code == 404

class TestShoppingListCollection(object):
    RESOURCE_URL = "/api/users/test_user1/shoppinglists/"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)



class TestShoppingListItem(object):
    RESOURCE_URL = "/api/users/test_user1/shoppinglists/personal"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)

    def test_delete(self, client):
        # valid delete
        response = client.delete(self.RESOURCE_URL)
        assert response.status_code == 204

        # try to delete same shopping list again
        response = client.delete(self.RESOURCE_URL)
        assert response.status_code == 404


class TestShoppingListFoodItems(object):
    RESOURCE_URL = "/api/users/test_user1/shoppinglists/personal/glenlivet"


    def test_delete(self, client):
        # valid delete
        response = client.delete(self.RESOURCE_URL)
        assert response.status_code == 204

        # try to delete same shopping list item again
        response = client.delete(self.RESOURCE_URL)
        assert response.status_code == 404

class TestPantryCollection(object):
    RESOURCE_URL = "/api/users/test_user1/pantry/"


    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)

class TestPantryFoodItemItem(object):
    RESOURCE_URL = "/api/users/test_user1/pantry/redbull"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)

class TestFoodItemCollection(object):
    RESOURCE_URL = "/api/fooditems/"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)

class TestFoodItemItem(object):
    RESOURCE_URL = "/api/fooditems/asahi"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        _check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)
