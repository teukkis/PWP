from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Recipes(db.Model):

    #table definition

    

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["recipe"]
        }
        props = schema["properties"] = {}
        props["recipe"] = {
            "description": "",
            "type": "string"
        }
        return schema
