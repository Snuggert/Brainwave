"""product.py - API calls for products."""
from brainwave import db
from brainwave.models import Product


class ProductAPI:
    """The API for product manipulation."""
    @staticmethod
    def create(product_dict):
        """Create product."""
        product = Product.new_dict(product_dict)

        db.session.add(product)
        db.session.commit()

        return product

    @staticmethod
    def get(product_id):
        """Get a product by its id."""
        return Product.query.get(product_id)

    @staticmethod
    def get_all():
        """Get all product items."""
        return Product.query.all()

    @staticmethod
    def delete(product):
        """ Delete product item """
        db.session.delete(product)
        db.session.commit()
