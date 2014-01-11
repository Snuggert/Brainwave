"""product_category.py - API calls for products."""
from brainwave import db
from brainwave.models import ProductCategory
from brainwave.utils import row2dict


class ProductCategoryAPI:
    """The API for product category manipulation."""
    @staticmethod
    def create(product_category_dict):
        """ Create product category"""
        product_category = ProductCategory.new_dict(product_category_dict)
        db.session.add(product_category)
        db.session.commit()

        return row2dict(product_category)

    @staticmethod
    def get(product_category_id):
        """ Get a product category by its id """
        product_category = ProductCategory.query.get(product_category_id)
        if product_category is None:
            return None
        else:
            return row2dict(product_category)

    @staticmethod
    def get_all():
        """ Get all product items """
        product_categories = ProductCategory.query.all()
        return_product_categories = []
        for item in product_categories:
            dictitem = row2dict(item)
            return_product_categories.append(dictitem)
        return return_product_categories

    @staticmethod
    def delete(item):
        """ Delete product item """
        if type(item) is dict:
            item = ProductCategory.by_id(item['id'])
        db.session.delete(item)
        db.session.commit()
        return