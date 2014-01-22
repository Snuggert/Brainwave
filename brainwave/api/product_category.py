"""product_category.py - Controller for ProductCategory."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import ProductCategoryController
from brainwave.utils import serialize_sqla
from brainwave.models import User
from brainwave.controllers.authentication import Authentication

product_category_api = Blueprint('product_category_api', __name__,
                                 url_prefix='/api/product_category')


@product_category_api.route('', methods=['POST'])
@Authentication(User.ROLE_ASSOCIATION)
def create():
    """Create new product category."""
    product_category = request.json

    product_category = ProductCategoryController.create(product_category)

    return jsonify(id=product_category.id)


@product_category_api.route('/<int:product_category_id>', methods=['DELETE'])
@Authentication(User.ROLE_ASSOCIATION)
def delete(product_category_id):
    """Delete product category."""
    product_category = ProductCategoryController.get(product_category_id)

    if not product_category:
        return jsonify(error='Product category not found'), 500

    ProductCategoryController.delete(product_category)

    return jsonify()


@product_category_api.route('/<int:product_category_id>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get(product_category_id):
    """Get product category."""
    product_category = ProductCategoryController.get(product_category_id)

    if not product_category:
        return jsonify(error='Product category not found'), 500

    return jsonify(product_category=serialize_sqla(product_category))
