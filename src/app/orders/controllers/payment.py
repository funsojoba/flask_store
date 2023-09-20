from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.orders.services.payment import PaymentService
from core.utils import Response


class PaymentController(Resource):
    payment_service = PaymentService()

    @jwt_required()
    def post(self, cart_id):
        self.payment_service.process_payment(cart_id)

        return Response(success=True, message="Payment successful", status_code=200)
