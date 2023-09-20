import json

from celery import shared_task

from app.core.resources.cache import redis_cache
from app.core.resources.nourish_me_api import requests
from app.core.utils import MENU_URL, PLACE_ORDERS_URL


@shared_task
def process_order(order_id):

    cache = redis_cache()
    employees = cache.get(order_id)
    if not employees:
        return {"status": "error", "message": "Order not found"}

    # Fetch menu items
    menu = requests.get(MENU_URL).get("dishes")

    menu_map = {dish["name"]: dish["id"] for dish in menu}

    # Transform employee list to order format
    orders = []
    for employee in employees["Employees"]["Employee"]:
        if employee["IsAttending"] == "false":
            continue

        order = {}
        order["customer"] = {
            "name": employee["Name"],
            "address": {
                "street": employee["Address"]["Street"],
                "city": employee["Address"]["City"],
                "postal_code": employee["Address"]["PostalCode"],
            },
        }
        order["items"] = []

        for dish in employee["Order"].split(", "):
            amount, name = dish.split("x ")
            order["items"].append({"id": menu_map[name], "amount": int(amount)})

        orders.append(order)

    data = json.dumps({"orders": orders})

    response = requests.post(PLACE_ORDERS_URL, json=data)
    cache.delete(order_id)
    return response
