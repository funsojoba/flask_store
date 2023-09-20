from app.orders.models import CartItem
from app.orders.services.cart import CartService
from app.products.services.product import ProductService
from core.error_handlers import AppError
from core.utils import BaseService


class CartItemService(BaseService):
    model = CartItem
    product_service = ProductService()
    cart_service = CartService()

    def get_all(self, cart_id):
        return self.model.query.filter_by(cart_id=cart_id).all()

    def create(self, cart_id, cart_item_data):
        product_id = cart_item_data.get("product_id")
        product_quantity = cart_item_data.get("quantity")

        item_in_cart = self.model.query.filter_by(
            cart_id=cart_id, product_id=product_id
        ).first()
        if item_in_cart:
            raise AppError(400, "Item already in cart")

        product = self.check_stock(product_id, product_quantity, cart_id)

        cart_item_data.update({"cart_id": cart_id})
        cart_item = self.model(**cart_item_data)
        try:
            cart_item.save()
        except Exception as e:
            self.logger.error("CartItemService.create(): %s", e)
            raise AppError(500)

        product.quantity -= product_quantity

        try:
            product.save()
        except Exception as e:
            self.logger.error("CartItemService.create(): %s", e)
            raise AppError(500)

    def update(self, cart_id, cart_item_id, cart_item_data):
        cart_item = self.get(cart_id, cart_item_id)
        new_quantity = cart_item_data.get("quantity")
        product_id = cart_item_data.pop("product_id")

        if cart_item.quantity == new_quantity:
            return cart_item

        if cart_item.quantity > new_quantity:
            qty = cart_item.quantity - new_quantity
        else:
            qty = new_quantity - cart_item.quantity

        product = self.check_stock(product_id, qty, cart_id)
        decrease_qty = product.quantity - qty
        increase_qty = product.quantity + qty

        product.quantity = (
            increase_qty if cart_item.quantity > new_quantity else decrease_qty
        )
        try:
            product.save()
            cart_item.update(cart_item_data)
        except Exception as e:
            self.logger.error("CartItemService.update(): %s", e)
            raise AppError(500)

        return cart_item

    def get(self, cart_id, cart_item_id):
        cart_item = self.model.query.filter_by(id=cart_item_id, cart_id=cart_id).first()
        if not cart_item:
            raise AppError(404, "Cart item not found")

        return cart_item

    def delete(self, cart_id, cart_item_id):
        cart_item = self.get(cart_id, cart_item_id)
        product = self.product_service.get(cart_item.product_id)
        product.quantity += cart_item.quantity

        try:
            product.save()
            cart_item.delete()
        except Exception as e:
            self.logger.error("CartItemService.delete(): %s", e)
            raise AppError(500)

    def check_stock(self, product_id, product_quantity, cart_id):
        product = self.product_service.get(product_id)
        if not product.in_stock or product.quantity < product_quantity:
            raise AppError(400, "Product out of stock")

        cart = self.cart_service.get(cart_id)
        if cart.state == "COMPLETED":
            raise AppError(400, "Cannot add item to completed cart")

        return product
