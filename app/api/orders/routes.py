from app.api.orders.views import FoodOrderView


def init_api_routes(api):
    api.add_resource(FoodOrderView, "/v1/orders")
