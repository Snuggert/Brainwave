"""product.py - API calls for products."""
from brainwave import db
from brainwave.models import Product
from brainwave.utils import row2dict
from .stock import StockAPI
from .product_category import ProductCategoryAPI


class ProductAPI:
    """The API for product manipulation."""
    @staticmethod
    def create(product_dict):
        """ Create product"""
        product_dict['stock'] = StockAPI.get(product_dict['stock_id'])
        product_dict['product_category'] = ProductCategoryAPI.get(
            product_dict['product_category_id'])
        product = Product.new_dict(product_dict)
        db.session.add(product)
        db.session.commit()

        return row2dict(product)

    @staticmethod
    def get(product_id):
        """ Get a product by its id """
        product = Product.query.get(product_id)
        if product is None:
            return None
        product = row2dict(product)
        product['stock'] = StockAPI.get(product['stock_id'])
        product['product_category'] = ProductCategoryAPI.get(
            product['product_category_id'])
        return product

    @staticmethod
    def get_all():
        """ Get all product items """
        products = Product.query.all()
        return_products = []
        for item in products:
            dictitem = row2dict(item)
            dictitem['stock'] = StockAPI.get(dictitem['stock_id'])

            dictitem['product_category'] = ProductCategoryAPI.get(
                dictitem['product_category_id'])

            return_products.append(dictitem)
        return return_products

    @staticmethod
    def delete(item):
        """ Delete product item """
        if type(item) is dict:
            item = Product.by_id(item['id'])
        db.session.delete(item)
        db.session.commit()
        return