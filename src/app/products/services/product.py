from app.products.models import Product, ProductCategory, ProductLabel
from core.error_handlers import AppError
from core.utils.utils import BaseService


class ProductService(BaseService):
    model = Product

    def create(self, data):
        prod_labels = data.pop("labels")
        prod_category = data.pop("category").get("name")

        category = ProductCategory.query.filter_by(name=prod_category.upper()).first()
        if not category:
            category = ProductCategory(name=prod_category)
            try:
                category.save()
            except Exception as e:
                self.logger.error("ProductService.create(): %s", str(e))
                raise AppError(500)

        data.update({"category_id": category.id})

        product = self.model(**data)
        try:
            product.save()
        except Exception as e:
            self.logger.error("ProductService.create(): %s", str(e))
            raise AppError(500)

        for prod_label in prod_labels:
            label = ProductLabel(**prod_label, product_id=product.id)
            try:
                label.save()
            except Exception as e:
                self.logger.error("ProductService.create(): %s", str(e))
                raise AppError(500)

    def get_all(self):
        try:
            products = self.model.query.all()
        except Exception as e:
            self.logger.error("ProductService.get_all(): %s", str(e))
            raise AppError(500)

        return products

    def get(self, product_id):
        try:
            product = Product.query.filter_by(id=product_id).first()
        except Exception as e:
            self.logger.error("ProductService.get(): %s", str(e))
            raise AppError(500)

        if not product:
            raise AppError(404, "Product not found")

        return product

    def update(self, product_id, data):
        product = self.get(product_id)

        prod_category = data.pop("category", None)
        if prod_category:
            prod_category = prod_category.get("name")
            category = ProductCategory.query.filter_by(
                name=prod_category.upper()
            ).first()
            if not category:
                category = ProductCategory(name=prod_category)
                try:
                    category.save()
                except Exception as e:
                    self.logger.error("ProductService.update(): %s", str(e))
                    raise AppError(500)

            data.update({"category_id": category.id})
        try:
            product.update(data)
        except Exception as e:
            self.logger.error("ProductService.update(): %s", str(e))
            raise AppError(500)

    def delete(self, product_id):
        product = self.get(product_id)
        try:
            product.delete()
        except Exception as e:
            self.logger.error("ProductService.delete(): %s", str(e))
            raise AppError(500)
