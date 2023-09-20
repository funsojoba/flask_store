from uuid import uuid4

from flask import current_app


class Response:
    def __new__(cls, success, status_code, message, data=None, *args, **kwargs):
        response = cls.format(success, message, data)
        return response, status_code

    @classmethod
    def format(cls, success, message, data):
        return dict(success=success, message=message, data=data)


class BaseService:
    @property
    def logger(self):
        return current_app.logger


def validate_file(data):
    result = {
        "status": True,
        "message": "Order validated successfully",
    }

    if not data or not data.get("order", None):
        result.update({"message": "No file uploaded", "status": False})
        return result
    _file = data.get("order")

    if _file.content_type != "application/xml":
        result.update({"message": "Invalid file type", "status": False})

    return result


def generate_temp_id():
    return str(uuid4())
