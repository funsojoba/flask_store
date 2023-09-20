from marshmallow import fields

from core.utils import CamelCaseSchema


class ListSchema(CamelCaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class ProductCategorySchema(ListSchema):
    pass


class ProductLabelSchema(ListSchema):
    value = fields.String(required=True)


class ProductSchema(CamelCaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    price = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    category = fields.Nested(ProductCategorySchema, required=True)
    labels = fields.List(fields.Nested(ProductLabelSchema), required=True)
    in_stock = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
