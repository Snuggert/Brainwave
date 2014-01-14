"""transaction.py - Transaction for user."""
from flask import Blueprint, jsonify, request
from brainwave.controllers.transaction import TransactionController
from brainwave.controllers.transaction_piece import TransactionPieceController
from brainwave.utils import serialize_sqla

transaction_api = Blueprint('transaction_api', __name__,
                            url_prefix='/api/transaction')


@transaction_api.route('/new', methods=['POST'])
def create():
    """Create a new transaction."""
    dict = request.json

    # Temporarily set assoc_id to 1, should be changed later
    transaction = TransactionController.create({'assoc_id':'1',
                                                'pay_type':dict['pay_type']})

    if not transaction:
        return jsonify(status='failed', error="Creation failed."), 500

    # Create individual transaction pieces
    for piece in dict['items']:
        # product_id and action are already known, add transaction_id and price
        piece['transaction_id'] = transaction.id
        piece['price'] = 2.00  # change later

        transaction_piece = TransactionPieceController.create(piece)

        if not transaction_piece:
            return jsonify(status='failed', error="Creation failed."), 500

    return jsonify(status='success')