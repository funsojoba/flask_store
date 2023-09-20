import json

import pytest

from app.core.resources.nourish_me_api import requests
from app.core.utils import DISHES_DATA, MENU_URL, PLACE_ORDERS_URL


@pytest.mark.parametrize(
    "url, data",
    [
        pytest.param(MENU_URL, {"dishes": DISHES_DATA}, id="valid-menu-url"),
        pytest.param(PLACE_ORDERS_URL, None, id="invalid-menu-url"),
    ],
)
def test_get_menu(url, data):
    """
    GIVEN the nourish.me API is running
    WHEN a GET request is made to the menu endpoint with a valid url
    THEN the response is a list of dishes
    """

    response = requests.get(url)

    assert response == data


@pytest.mark.parametrize(
    "url, payload, res",
    [
        pytest.param(
            PLACE_ORDERS_URL,
            json.dumps(
                {
                    "orders": [
                        {
                            "customer": {
                                "name": "John Doe",
                                "address": {
                                    "street": "123 Main St",
                                    "city": "New York",
                                    "postal_code": "10001",
                                },
                            },
                            "items": [{"id": 1, "amount": 1}],
                        }
                    ]
                }
            ),
            {"status": "success", "message": "Order created successfully"},
            id="valid-order",
        ),
        pytest.param(
            MENU_URL,
            json.dumps(
                {
                    "orders": [
                        {
                            "customer": {
                                "name": "John Doe",
                                "address": {
                                    "street": "123 Main St",
                                    "city": "New York",
                                    "postal_code": "10001",
                                },
                            },
                            "items": [{"id": 1, "amount": 1}],
                        }
                    ]
                }
            ),
            None,
            id="invalid-order-url",
        ),
    ],
)
def test_place_orders(url, payload, res):
    """
    GIVEN the nourish.me API is running
    WHEN a POST request is made to the orders endpoint with a valid url
    THEN the response is a success message
    """

    response = requests.post(url, json=payload)

    assert response == res
