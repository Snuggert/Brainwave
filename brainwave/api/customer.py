"""customer.py - Controller for customer."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import CustomerController
from brainwave.utils import serialize_sqla

customer_api = Blueprint('customer_api', __name__,
                         url_prefix='/api/customer')


@customer_api.route('', methods=['POST'])
def create():
    """Create a new customer."""
    customer_dict = request.json

    customer = CustomerController.create(customer_dict)

    return jsonify(id=customer.id)


@customer_api.route('/<int:customer_id>', methods=['PUT'])
def update(customer_id):
    """Update a customer."""
    customer_dict = request.json

    CustomerController.update(customer_dict)

    return jsonify()


@customer_api.route('/<int:customer_id>', methods=['DELETE'])
def delete(customer_id):
    """Delete a customer."""
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    CustomerController.delete(customer)

    return jsonify()


@customer_api.route('/<int:customer_id>', methods=['GET'])
def get(customer_id):
    """Get a customer."""
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    return jsonify(customer=serialize_sqla(customer))
