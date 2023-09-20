import pytest

from app.core.resources.cache import redis_cache


def test_cache():
    """
    GIVEN the cache is running
    WHEN a value is set
    THEN the value is returned
    """

    cache = redis_cache()

    value = {"id": 1, "first_name": "John", "last_name": "Doe"}
    cache.set("test", value)

    expected_value = cache.get("test")

    assert value == expected_value
