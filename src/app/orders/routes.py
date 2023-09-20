from app.orders.controllers.cart import CartController, CartDetailController
from app.orders.controllers.cart_item import (
    CartItemController,
    CartItemDetailController,
)
from app.orders.controllers.payment import PaymentController


def init_cart_routes(api):
    api.add_resource(CartController, "/v1/cart")
    api.add_resource(CartDetailController, "/v1/cart/<int:cart_id>")
    api.add_resource(CartItemController, "/v1/cart/<int:cart_id>/items")
    api.add_resource(
        CartItemDetailController, "/v1/cart/<int:cart_id>/items/<int:cart_item_id>"
    )
    api.add_resource(PaymentController, "/v1/cart/<int:cart_id>/payment")
