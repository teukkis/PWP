from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class FoodItem(db.Model):

    #table definition

    

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["food_item_name"]
        }
        props = schema["properties"] = {}
        props["food_item_name"] = {
            "description": "",
            "type": "string"
        }
        return schema
