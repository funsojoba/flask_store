from marshmallow import fields

from core.utils.utils import CamelCaseSchema


class LoginSchema(CamelCaseSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class LoginResponseSchema(CamelCaseSchema):
    access_token = fields.String(required=True)
