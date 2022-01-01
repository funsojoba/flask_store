import os
from flask import Flask
from src.auth import auth

from src.database import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRETE_KEY=os.environ.get("SECRETE_KEY") or "dev",
            SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(app.instance_path, "database.db"),
        )
    else:
        app.config.from_mapping(test_config)
    
    db.app = app
    db.init_app(app)
    app.register_blueprint(blueprint=auth)
    return app



