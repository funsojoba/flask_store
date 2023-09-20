from marshmallow import fields

from core.utils import CamelCaseSchema


class CartSchema(CamelCaseSchema):
    id = fields.Integer()
    is_paid = fields.Boolean(dump_only=True)
    quantity = fields.Integer()
    total_amount = fields.Integer()
    total_quantity = fields.Integer()
    state = fields.String(dump_only=True)
    cart_items = fields.Nested("CartItemSchema", many=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CartItemSchema(CamelCaseSchema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True)
    product_name = fields.String(dump_only=True)
    quantity = fields.Integer(required=True)
    amount = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
