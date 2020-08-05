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
    # create two users
    for i in range(1, 3):
        user = User(
                username="test_user{}".format(i),
                email="test{}@test.com".format(i)
                )
        db.session.add(user)
    db.session.commit()

def _check_namespace(client, response):
    """
    Test that "foodman" namespace is found in the response and
    and the href value can be used to get a valid response.
    """
    print(response)
    namespace_href = response["@namespaces"]["foodman"]["name"]
    print(namespace_href)
    resp = client.get(namespace_href)
    assert resp.status_code == 200

def _check_control_get(ctrl, client, obj):
    """
    Tests the existence of a control that uses get method
    and also that the href of the control works.
    """
    print(dict(obj).keys())
    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200

def _get_user_json():
    """
    Creates a dummy user json to be used in tests.
    """
    return {"username": "dummy_user", "email": "dummy@user.com"}

class TestUserCollection(object):
    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        #_check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)
        assert len(resp_body["items"]) == 2
        for item in resp_body["items"]:
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
    RESOURCE_URL = "/api/users/test_user1"

    def test_get(self, client):
        response = client.get(self.RESOURCE_URL)
        assert response.status_code == 200
        resp_body = json.loads(response.data)
        #_check_namespace(client, resp_body)
        _check_control_get("self", client, resp_body)
        _check_control_get("collection", client, resp_body)
        #_check_control_get("foodman:add-user", client, resp_body)

class TestShoppingListCollection(object):
    RESOURCE_URL = "/api/users/test_user01/shoppinglists/"




class TestShoppingListItem(object):
    RESOURCE_URL = "/api/users/test_user01/shoppinglists/personal/"


class TestShoppingListFoodItems(object):
    RESOURCE_URL = "/api/users/test_user01/shoppinglists/personal/whisky/"


class TestPantryCollection(object):
    RESOURCE_URL = "/api/users/test_user01/pantry/"


class TestPantryFoodItemItem(object):
    RESOURCE_URL = "/api/users/test_user01/pantry/redbull/"


class TestFoodItemCollection(object):
    RESOURCE_URL = "/api/fooditems/"


class TestFoodItemItem(object):
    RESOURCE_URL = "/api/fooditems/asahi/"
