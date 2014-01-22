"""product.py - Controller for Product."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import ProductController
from brainwave.utils import serialize_sqla
from brainwave.controllers.authentication import Authentication
from brainwave.models import User

product_api = Blueprint('product_api', __name__,
                        url_prefix='/api/product')


@product_api.route('', methods=['POST'])
@Authentication(User.ROLE_ASSOCIATION)
def create():
    """ Create new product """
    product_dict = request.json
    if product_dict:
        if product_dict['price'] == '':
            product_dict['price'] = 0.0
        if product_dict['volume'] == '':
            product_dict['product_dict'] = 0.0
    print product_dict
    product = ProductController.create(product_dict)
    return jsonify(id=product.id)


@product_api.route('/<int:product_id>', methods=['DELETE'])
@Authentication(User.ROLE_ASSOCIATION)
def delete(product_id):
    """ Delete product """
    product = ProductController.get(product_id)

    if not product:
        return jsonify(error='Product not found'), 500

    ProductController.delete(product)

    return jsonify()


@product_api.route('/<int:product_id>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get(product_id):
    """ Get product """
    product = ProductController.get(product_id)

    if not product:
        return jsonify(error='Product not found'), 500

    return jsonify(product=serialize_sqla(product))


@product_api.route('/all', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_all():
    """ Get all products unfiltered """
    # At this point, the association_id should be gotten, so that not ALL
    # products are listed, but only those related to the relevant association.
    products = ProductController.get_all()

    if not products:
        return jsonify(error='No products were found'), 500

    return jsonify(products=serialize_sqla(products))


@product_api.route('/search/', methods=['GET'])  # temp
@product_api.route('/search/<string:query>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_all_from(query=""):
    """ Get all products objects filter by query """
    if query == "":
        products = ProductController.get_all()
    else:
        products = ProductController.get_all_from(query)
    # stock = StockController.get_all()

    if not products:
        return jsonify(error='Product item not found'), 200

    return jsonify(products=serialize_sqla(products))
