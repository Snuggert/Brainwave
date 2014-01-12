"""customer.py - Controller for customer."""
from flask import Blueprint, jsonify, request
from brainwave.api.customer import CustomerAPI
from brainwave.utils import serialize_sqla

customer_controller = Blueprint('customer_controller', __name__,
                                url_prefix='/api/customer')


@customer_controller.route('', methods=['POST'])
def create():
    """Create a new customer."""
    customer_dict = request.json

    customer = CustomerAPI.create(customer_dict)

    return jsonify(id=customer.id)


@customer_controller.route('/<int:customer_id>', methods=['PUT'])
def update(customer_id):
    """Update a customer."""
    customer_dict = request.json

    CustomerAPI.update(customer_dict)

    return jsonify()


@customer_controller.route('/<int:customer_id>', methods=['DELETE'])
def delete(customer_id):
    """Delete a customer."""
    customer = CustomerAPI.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    CustomerAPI.delete(customer)

    return jsonify()


@customer_controller.route('/<int:customer_id>', methods=['GET'])
def get(customer_id):
    """Get a customer."""
    customer = CustomerAPI.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    return jsonify(customer=serialize_sqla(customer))
