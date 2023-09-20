from flask import request
from flask_restful import Resource

from app.api.orders.schema import OrderSchema
from app.api.orders.services import FoodOrderService
from app.core.utils import Response
from app.core.utils.utils import validate_file


class FoodOrderView(Resource):
    service = FoodOrderService()

    def post(self):
        order = OrderSchema().load(request.files)
        error = validate_file(order)
        if not error.get("status"):
            return Response(
                success=False, message=error.get("message"), status_code=400
            )
        self.service.create(order)

        return Response(
            success=True, message="Order created successfully", status_code=201
        )
