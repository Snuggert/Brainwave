""" product_category.py - Controller for ProductCategory. """
from flask import Blueprint, jsonify, request
from brainwave.api import ProductCategoryAPI
from brainwave.utils import serialize_sqla

product_category_controller = Blueprint('product_category_controller',
                                        __name__,
                                        url_prefix='/api/product_category')


@product_category_controller.route('', methods=['POST'])
def create():
    """ Create new product category """
    product_category = request.json

    product_category = ProductCategoryAPI.create(product_category)

    return jsonify(id=product_category['id'], name=product_category['name'])


@product_category_controller.route('/<int:product_category_id>',
                                   methods=['DELETE'])
def delete(product_category_id):
    """ Delete product category """
    product_category = ProductCategoryAPI.get(product_category_id)

    if not product_category:
        return jsonify(error='Product category not found'), 500

    ProductCategoryAPI.delete(product_category)

    return jsonify()


@product_category_controller.route('/<int:product_category_id>',
                                   methods=['GET'])
def get(product_category_id):
    """ Get product category"""
    product_category = ProductCategoryAPI.get(product_category_id)

    if not product_category:
        return jsonify(error='Product category not found'), 500

    return jsonify(product_category=serialize_sqla(product_category))