import logging

from dateutil.relativedelta import *
from dateutil.rrule import *
from flask import current_app
from flask_restful import Resource
from marshmallow import Schema

logger = logging.getLogger(__name__)


class Response(Resource):
    def __new__(cls, success, status_code, message, data=None, *args, **kwargs):
        response = cls.format(success, message, data)
        return response, status_code

    @classmethod
    def format(cls, success, message, data):
        return dict(success=success, message=message, data=data)


def to_camel_case(string):
    parts = iter(string.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = to_camel_case(field_obj.data_key or field_name)

    class Meta:
        ordered = True


def cast_str(value):
    try:
        return str(value) if value is not None else None
    except ValueError:
        return None


class BaseService:
    @property
    def logger(self):
        return current_app.logger
