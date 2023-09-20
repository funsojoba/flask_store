from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

import core.settings as config
from app.orders.schema import CartSchema
from app.orders.services.cart import CartService
from core.resources.jwt import JWTClient
from core.utils import Response


class CartController(Resource):
    cart_service = CartService()
    jwt_client = JWTClient(config)

    @jwt_required()
    def get(self):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)

        carts = self.cart_service.get_all(user_id)
        cart_schema = CartSchema(many=True)
        carts = cart_schema.dump(carts)

        return Response(
            success=True, message="Carts returned", data=carts, status_code=200
        )

    @jwt_required()
    def post(self):
        jwt_identity = get_jwt_identity()
        user_id = self.jwt_client.get_user_id(jwt_identity)
        cart_id = self.cart_service.create(user_id)

        return Response(
            success=True, message="Cart created", data=cart_id, status_code=201
        )


class CartDetailController(Resource):
    cart_service = CartService()

    @jwt_required()
    def get(self, cart_id):
        cart = self.cart_service.get(cart_id)
        cart_schema = CartSchema()
        cart = cart_schema.dump(cart)

        return Response(
            success=True, message="Cart returned", data=cart, status_code=200
        )
