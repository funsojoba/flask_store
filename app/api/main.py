import logging

from celery import Celery
from flask import Flask, json
from flask_cors import CORS
from flask_restful import Api
from marshmallow.exceptions import ValidationError
from werkzeug.wrappers import Response

import app.core.settings as config
from app.api.orders.routes import init_api_routes
from app.core.error_handlers import AppError


class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.logger = logging.getLogger("gunicorn.error")

    def load_config(self):
        # load flask config from settings
        for k in dir(config):
            v = getattr(config, k)
            if not k.startswith("_") and k.upper() == k and not callable(v):
                self.app.config[k] = v

    def build_app(self):
        self.load_config()
        # set logging based on unicorn level
        self.app.logger.handlers = self.logger.handlers
        if __name__ != "main":
            self.app.logger.setLevel(self.logger.level)
        else:
            self.app.logger.setLevel(logging.DEBUG)
        self.app.logger.info(
            "Logger Configured w/level {}".format(self.app.logger.level)
        )

        CORS(self.app)
        self.set_routes()
        self.celery()

        return self.app

    def set_routes(self):
        api = Api(self.app)
        init_api_routes(api)
        self.set_home_route()

    def set_home_route(self):
        @self.app.route("/")
        def home():
            return json.dumps({"status": True, "message": "Welcome to the API"})

    def get_app(self):
        return self.app

    def celery(self):
        celery = Celery(
            self.app.import_name,
            backend=config.CELERY_RESULT_BACKEND,
            broker=config.CELERY_BROKER_URL,
        )
        celery.conf.update(self.app.config)

        celery.set_default()
        return celery


# =============================================================================

app = App().build_app()
celery = App().celery()

# =============================================================================
@app.errorhandler(AppError)
def handle_exception(error):
    payload = {"success": error.success, "data": error.data}
    if getattr(error, "message", None):
        payload["message"] = error.message

    response = Response()

    response.data = json.dumps(payload)
    response.content_type = "application/json"
    response.status_code = error.code
    return response


@app.errorhandler(ValidationError)
def schema_validation_error(error):
    payload = {
        "success": False,
        "message": "Validation Error",
        "errors": error.messages,
    }
    response = Response()
    response.content_type = "application/json"
    response.data = json.dumps(payload)
    response.status_code = 400
    app.logger.error(error)
    return response
