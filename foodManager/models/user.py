from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):

    #table definition



    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["username"]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "description": "",
            "type": "string"
        }
        return schema
