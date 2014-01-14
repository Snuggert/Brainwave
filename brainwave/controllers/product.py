"""product.py - Controller calls for products."""
from brainwave import db
import difflib
from brainwave.models import Product


class ProductController:
    """The Controller for product manipulation."""
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
    def get_all_from(query):
        """ Get all product objects searched by query """

        products = Product.query.all()
        items = [item.name for item in products]

        result_names = difflib.get_close_matches(query, items, len(items),
                                                 0.25)

        results = Product.query.filter(Product.name.in_(result_names)).all()

        return results

    @staticmethod
    def delete(product):
        """ Delete product item """
        db.session.delete(product)
        db.session.commit()
