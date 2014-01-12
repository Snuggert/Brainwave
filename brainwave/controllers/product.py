"""product.py - Controller for Product."""
from flask import Blueprint, jsonify, request
from brainwave.api import ProductAPI
from brainwave.utils import serialize_sqla

product_controller = Blueprint('product_controller', __name__,
                               url_prefix='/api/product')


@product_controller.route('', methods=['POST'])
def create():
    """ Create new product """
    product_dict = request.json
    print product_dict
    product = ProductAPI.create(product_dict)
    return jsonify(id=product.id)


@product_controller.route('/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    """ Delete product """
    product = ProductAPI.get(product_id)

    if not product:
        return jsonify(error='Product not found'), 500

    ProductAPI.delete(product)

    return jsonify()


@product_controller.route('/<int:product_id>', methods=['GET'])
def get(product_id):
    """ Get product """
    product = ProductAPI.get(product_id)

    if not product:
        return jsonify(error='Product not found'), 500

    return jsonify(product=serialize_sqla(product))
