import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from foodManager.constants import *
from flask_cors import CORS


db = SQLAlchemy()

# Based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory
# Modified to use Flask SQLAlchemy

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///dev.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from . import models
    from . import api
    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.generate_test_data)
    app.register_blueprint(api.api_bp)

    @app.route(LINK_RELATIONS_URL)

    def send_link_relations():
        return "Link relations: .."


    @app.route("/profiles/<profile>")

    def send_profile(profile):
        return "You requested profile {}".format(profile)

    return app
