"""transaction.py - Transaction for user."""
from flask import Blueprint, jsonify, request
from brainwave.controllers.transaction import TransactionController
from brainwave.utils import serialize_sqla

transaction_api = Blueprint('transaction_api', __name__,
                            url_prefix='/api/transaction')


@transaction_api.route('/new', methods=['POST'])
def create():
    """Create a new transaction."""
    dict = request.json

    transaction = TransactionController.create(dict)

    if not transaction:
        return jsonify(status='failed', error="No transaction found."), 500

    return jsonify(status='success')
