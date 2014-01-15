"""credit.py - API for credit."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import CreditController, CustomerController
from brainwave.utils import serialize_sqla

credit_api = Blueprint('credit_api', __name__, url_prefix='/api/credit')


@credit_api.route('', methods=['POST'])
def create():
    """Create a new credit."""
    credit_dict = request.json

    try:
        credit = CreditController.create(credit_dict)
    except CustomerController.AssociationNotCoupled() as e:
        return jsonify(error=e.error), 500

    return jsonify(id=credit.id)


@credit_api.route('/<credit_id>', methods=['GET'])
def get(credit_id):
    """Get a credit by its id."""
    credit = CreditController.get(credit_id)

    if not credit:
        return jsonify(error='Credit not found'), 500

    return jsonify(credit=serialize_sqla(credit))


@credit_api.route('/add/<credit_id>', methods=['POST'])
def add(credit_id):
    """Add to the credit."""
    credit = CreditController.get(credit_id)

    if not credit:
        return jsonify(error='Credit not found'), 500

    amount = request.json['amount']
    CreditController.add(credit, amount)

    return jsonify(new_credit=credit.credit)


@credit_api.route('/<credit_id>', methods=['DELETE'])
def delete(credit_id):
    """Delete a credit."""
    credit = CreditController.get(credit_id)

    if not credit:
        return jsonify(error='Credit not found'), 500

    CreditController.delete(credit)

    return jsonify()
