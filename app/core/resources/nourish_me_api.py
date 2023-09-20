from functools import lru_cache

from app.api.orders.schema import NourishMeApiSchema
from app.core.utils import DISHES_DATA, MENU_URL, PLACE_ORDERS_URL


class RequestsMock:
    def __init__(self):
        self.dishes = DISHES_DATA

    def get(self, url):
        if url == MENU_URL:
            return {"dishes": self.dishes}
        return None

    def post(self, url, json):
        if url == PLACE_ORDERS_URL:
            try:
                NourishMeApiSchema().loads(json)
            except Exception as e:
                return {"status": "error", "message": str(e)}
            return {"status": "success", "message": "Order created successfully"}
        return None


@lru_cache()
def requests_mock():
    return RequestsMock()


requests = requests_mock()
