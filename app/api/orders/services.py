import xmltodict

from app.api.orders.tasks import process_order
from app.core.resources.cache import redis_cache
from app.core.utils.utils import BaseService, generate_temp_id


class FoodOrderService(BaseService):
    cache = redis_cache()

    def create(self, data):
        _file = data.get("order")

        file_data = _file.read().decode("utf-8")

        order = xmltodict.parse(file_data)
        order_id = f"order_{generate_temp_id()}"
        self.cache.set(order_id, order)

        process_order.delay(order_id)
