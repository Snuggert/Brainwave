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
    if product_dict:
        if product_dict['price'] == '':
            product_dict['price'] = 0.0
        if product_dict['volume'] == '':
            product_dict['product_dict'] = 0.0
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


@product_controller.route('/all', methods=['GET'])
def get_all():
    """ Get all products unfiltered """
    # At this point, the association_id should be gotten, so that not ALL
    # products are listed, but only those related to the relevant association.
    products = ProductAPI.get_all()

    if not products:
        return jsonify(error='No products were found'), 500

    return jsonify(products=serialize_sqla(products))
