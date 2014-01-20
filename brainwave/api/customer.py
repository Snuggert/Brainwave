"""customer.py - API for customer."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import CustomerController, AssociationController
from brainwave.utils import serialize_sqla

customer_api = Blueprint('customer_api', __name__,
                         url_prefix='/api/customer')


@customer_api.route('', methods=['POST'])
def create():
    """Create a new customer."""
    customer_dict = request.json

    try:
        customer = CustomerController.create(customer_dict)
    except CustomerController.NoNameGiven as e:
        return jsonify(error=e.error), 500

    return jsonify(id=customer.id)


@customer_api.route('/<int:customer_id>', methods=['PUT'])
def update(customer_id):
    """Update a customer."""
    customer_dict = request.json

    try:
        CustomerController.update(customer_dict)
    except CustomerController.NoNameGiven as e:
        return jsonify(error=e.error), 500

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


@customer_api.route('/all', methods=['GET'])
def get_all():
    """Get all customers."""
    customers = CustomerController.get_all()

    return jsonify(customers=serialize_sqla(customers))


@customer_api.route('/association/<int:customer_id>', methods=['GET'])
def get_associations(customer_id):
    """Get associations the customer is coupled to."""
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    associations = CustomerController.get_associations(customer).all()

    return jsonify(associations=serialize_sqla(associations))


@customer_api.route('/association/<int:customer_id>', methods=['POST'])
def add_association(customer_id):
    """Couple an association to the customer."""
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found')

    association_id = request.json['association_id']
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found')

    try:
        CustomerController.add_association(customer, association)
    except CustomerController.AssociationAlreadyCoupled as e:
        return jsonify(error=e.error)

    return jsonify()


@customer_api.route('/association/<int:customer_id>', methods=['DELETE'])
def remove_association(customer_id):
    """Remove an association the customer is coupled to."""
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found')

    association_id = request.json['association_id']
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found')

    try:
        CustomerController.remove_association(customer, association)
    except CustomerController.AssociationNotCoupled as e:
        return jsonify(error=e.error)

    return jsonify()
