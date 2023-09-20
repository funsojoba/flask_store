from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.products.schema import ProductLabelSchema
from app.products.services.product_label import ProductLabelService
from core.utils import Response


class ProductLabelController(Resource):
    product_label_service = ProductLabelService()

    @jwt_required()
    def get(self, product_id):
        labels = self.product_label_service.get_all(product_id)
        labels = ProductLabelSchema(many=True).dump(labels)

        return Response(
            success=True,
            message="Product labels retrieved",
            data=labels,
            status_code=200,
        )

    @jwt_required()
    def post(self, product_id):
        data = ProductLabelSchema().load(request.json)
        self.product_label_service.create(product_id, data)

        return Response(
            success=True, message="Product label created successfully", status_code=201
        )


class ProductLabelDetailController(Resource):
    product_label_service = ProductLabelService()

    @jwt_required()
    def get(self, product_id, label_id):
        label = self.product_label_service.get(product_id, label_id)
        label = ProductLabelSchema().dump(label)

        return Response(
            success=True,
            message="Product label retrieved successfully",
            data=label,
            status_code=200,
        )

    @jwt_required()
    def patch(self, product_id, label_id):
        data = ProductLabelSchema(partial=True).load(request.json)
        self.product_label_service.update(product_id, label_id, data)

        return Response(
            success=True, message="Product label updated successfully", status_code=200
        )

    @jwt_required()
    def delete(self, product_id, label_id):
        self.product_label_service.delete(product_id, label_id)

        return Response(
            success=True, message="Product label deleted successfully", status_code=200
        )
