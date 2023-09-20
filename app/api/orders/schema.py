import marshmallow


class OrderSchema(marshmallow.Schema):
    order = marshmallow.fields.Raw(type="file")


class AddressSchema(marshmallow.Schema):
    street = marshmallow.fields.String(required=True, allow_none=False)
    city = marshmallow.fields.String(required=True, allow_none=False)
    postal_code = marshmallow.fields.String(required=True, allow_none=False)


class CustomerSchema(marshmallow.Schema):
    name = marshmallow.fields.String(required=True, allow_none=False)
    address = marshmallow.fields.Nested(
        "AddressSchema", required=True, allow_none=False
    )


class OrderItemSchema(marshmallow.Schema):
    id = marshmallow.fields.Integer(required=True, allow_none=False)
    amount = marshmallow.fields.Integer(required=True, allow_none=False)


class ProcessOrdersSchema(marshmallow.Schema):
    customer = marshmallow.fields.Nested(
        "CustomerSchema", required=True, allow_none=False
    )
    items = marshmallow.fields.Nested(
        "OrderItemSchema", required=True, allow_none=False, many=True
    )


class NourishMeApiSchema(marshmallow.Schema):
    orders = marshmallow.fields.Nested(
        "ProcessOrdersSchema", required=True, allow_none=False, many=True
    )
