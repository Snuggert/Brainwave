"""association.py - Controller for association."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import AssociationController, CustomerController,\
    UserController
from brainwave.utils import serialize_sqla
from brainwave.controllers.authentication import Authentication
from brainwave.models.user import User

association_api = Blueprint('association_api', __name__,
                            url_prefix='/api/association')


@association_api.route('', methods=['POST'])
def create():
    """Create a new association."""
    association_dict = request.json

    try:
        association = AssociationController.create(association_dict)
    except AssociationController.NoNameGiven as e:
        return jsonify(error=e.error), 500
    except UserController.NoPassword as e:
        return jsonify(error=e.error), 500

    return jsonify(id=association.id)


@association_api.route('/<int:association_id>', methods=['PUT'])
@Authentication(User.ROLE_ASSOCIATION)
def update(association_id):
    """Update an association."""
    association_dict = request.json

    try:
        AssociationController.update(association_dict)
    except AssociationController.NoNameGiven as e:
        return jsonify(error=e.error), 500

    return jsonify()


@association_api.route('/<int:association_id>', methods=['DELETE'])
def delete(association_id):
    """Delete an association."""
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    AssociationController.delete(association)

    return jsonify()


@association_api.route('/<int:association_id>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get(association_id):
    """Get an association."""
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    return jsonify(association=serialize_sqla(association))


@association_api.route('/all', methods=['GET'])
def get_all():
    """Get all associations."""
    associations = AssociationController.get_all()

    return jsonify(associations=serialize_sqla(associations))


@association_api.route('/customer/<int:association_id>', methods=['GET'])
def get_customers(association_id):
    """Get customers the associations is coupled to."""
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    customers = AssociationController.get_customers(association).all()

    return jsonify(customers=serialize_sqla(customers))


@association_api.route('/customer/<int:association_id>', methods=['POST'])
def add_customer(association_id):
    """Couple a customer to the association."""
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    customer_id = request.json['customer_id']
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    try:
        AssociationController.add_customer(association, customer)
    except AssociationController.CustomerAlreadyCoupled as e:
        return jsonify(error=e.error), 500

    return jsonify()


@association_api.route('/customer/<int:association_id>', methods=['DELETE'])
def remove_customer(association_id):
    """Remove a customer the association is coupled to."""
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    customer_id = request.json['customer_id']
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    try:
        AssociationController.remove_customer(association, customer)
    except AssociationController.CustomerNotCoupled as e:
        return jsonify(error=e.error)

    return jsonify()
