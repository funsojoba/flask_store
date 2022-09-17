import os
from flask import Flask
from src.auth import auth


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRETE_KEY=os.environ.get("SECRETE_KEY") or "dev",
        )
    else:
        app.config.from_mapping(test_config)
    
    app.register_blueprint(blueprint=auth)
    return app



