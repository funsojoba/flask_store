from app.orders.models import Cart
from core.error_handlers import AppError
from core.utils.utils import BaseService


class CartService(BaseService):
    model = Cart

    def get_all(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def create(self, user_id):
        cart = self.model(user_id)
        try:
            cart.save()
        except Exception as e:
            self.logger.error("CartService.create(): %s", e)
            raise AppError(500)

        return {"id": cart.id}

    def get(self, cart_id):
        cart = self.model.query.filter_by(id=cart_id).first()
        if not cart:
            raise AppError(404, "Cart not found")

        return cart

    def update(self, cart_id, cart_data):
        cart = self.get(cart_id)
        try:
            cart.update(cart_data)
        except Exception as e:
            self.logger.error("CartService.update(): %s", e)
            raise AppError(500)

        return cart
