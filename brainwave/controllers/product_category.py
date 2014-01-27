"""product_category.py - Controller calls for product categories."""
from brainwave import db
from brainwave.models import ProductCategory


class ProductCategoryController:
    """The Controller for product category manipulation."""

    class NoNameGiven(Exception):
        """Exception for when no name is given for an product category."""
        def __init__(self):
            self.error = 'No name was given for the product category'

    @staticmethod
    def create(product_category_dict):
        """Create product category."""
        product_category = ProductCategory.new_dict(product_category_dict)

        db.session.add(product_category)
        db.session.commit()

        return product_category

    @staticmethod
    def update(product_category_dict):
        """Update the product_category."""

        product_category = ProductCategory.merge_dict(product_category_dict)

        if not product_category.name:
            raise ProductCategoryController.NoNameGiven()

        db.session.add(product_category)
        db.session.commit()

        return product_category

    @staticmethod
    def get(product_category_id):
        """ Get a product category by its id """
        return ProductCategory.query.get(product_category_id)

    @staticmethod
    def get_all():
        """ Get all product items """
        return ProductCategory.query.all()

    @staticmethod
    def delete(item):
        """ Delete product item """
        db.session.delete(item)
        db.session.commit()
