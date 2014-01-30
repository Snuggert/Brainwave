"""customer.py - API for customer."""
from flask import Blueprint, jsonify, request, session
from brainwave.controllers import CustomerController, AssociationController
from brainwave.utils import serialize_sqla
from brainwave.models import User, Association
from brainwave.controllers.authentication import Authentication
from brainwave.controllers.user import UserController

customer_api = Blueprint('customer_api', __name__,
                         url_prefix='/api/customer')


@customer_api.route('', methods=['POST'])
@Authentication(User.ROLE_ASSOCIATION)
def create():
    """Create a new customer."""
    customer_dict = request.json
    print customer_dict

    try:
        customer = CustomerController.create(customer_dict)
    except CustomerController.NoNameGiven as e:
        return jsonify(error=e.error), 500

    return jsonify(id=customer.id)


@customer_api.route('/<int:customer_id>', methods=['PUT'])
@Authentication(User.ROLE_ASSOCIATION)
def update(customer_id):
    """Update a customer."""
    customer_dict = request.json

    try:
        CustomerController.update(customer_dict)
    except CustomerController.NoNameGiven as e:
        return jsonify(error=e.error), 500

    return jsonify()


@customer_api.route('/<int:customer_id>', methods=['DELETE'])
@Authentication(User.ROLE_ASSOCIATION)
def delete(customer_id):
    """Delete a customer."""
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    CustomerController.delete(customer)

    return jsonify()


@customer_api.route('/<int:customer_id>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get(customer_id):
    """Get a customer."""
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    return jsonify(customer=serialize_sqla(customer))


@customer_api.route('/all/<scope>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_all(scope):
    """Get all customers."""
    if (scope == 'all'):
        # This means that the customers for ALL associations are fetched
        customers = CustomerController.get_all_all()
    else:
        # All customers from the current association are fetched
        customers = CustomerController.get_all()

    user_id = session['user_id']
    user = UserController.get(user_id)

    if not user.association:
        return jsonify(customers=serialize_sqla(customers))

    association = user.association[0]

    customer_dicts = []
    for customer in customers:
        customer_dict = serialize_sqla(customer)

        credit = customer.credits.filter(Association.id == association.id)\
            .first()
        if credit:
            customer_dict['credit'] = serialize_sqla(credit)
        else:
            customer_dict['credit'] = None

        customer_dicts.append(customer_dict)

    return jsonify(customers=customer_dicts)


@customer_api.route('/all', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_all_all():
    result = get_all('assoc')
    return result


@customer_api.route('/association/<int:customer_id>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_associations(customer_id):
    """Get associations the customer is coupled to."""
    customer = CustomerController.get(customer_id)

    if not customer:
        return jsonify(error='Customer not found'), 500

    associations = CustomerController.get_associations(customer).all()

    return jsonify(associations=serialize_sqla(associations))


@customer_api.route('/association/<int:customer_id>', methods=['POST'])
@Authentication(User.ROLE_ASSOCIATION)
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
@Authentication(User.ROLE_ASSOCIATION)
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
