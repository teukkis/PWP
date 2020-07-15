from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Shopping_list(db.Model):

    #table definition

    

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["list_name"]
        }
        props = schema["properties"] = {}
        props["list_name"] = {
            "description": "",
            "type": "string"
        }
        return schema
