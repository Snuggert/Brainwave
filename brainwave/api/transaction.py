"""transaction.py - Transaction for user."""
from flask import Blueprint, jsonify, request
from brainwave.utils import serialize_sqla, row2dict
from brainwave.controllers.transaction import TransactionController
from brainwave.controllers.authentication import Authentication
from brainwave.models import User

transaction_api = Blueprint('transaction_api', __name__,
                            url_prefix='/api/transaction')


# Dictionary format example:
# {
#    "pay_type":"cash",
#    "action":"sell",
#    "items":[
#       {
#          "product_id":"1",
#          "quantity": "7"
#       },
#       {
#          "product_id":"2",
#          "quantity": "100"
#       }
#    ]
# }
#
# pay_type can be either cash or pin (credit should become option 3, later)
# action can be sell, refund or gift
@transaction_api.route('', methods=['POST'])
@Authentication(User.ROLE_ASSOCIATION)
def create():
    """Create a new transaction."""
    transaction_dict = request.json

    # Note that the TransactionController creates records for both the
    # Transaction table as the TransactionPiece table.
    transaction = TransactionController.create(transaction_dict)

    if not transaction:
        return jsonify(status='failed', error="Could not sell items."), 500

    return jsonify(status='success')


@transaction_api.route('/<int:transaction_id>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get(transaction_id):
    """Get trans_in item."""
    transaction = TransactionController.get(transaction_id)
    if not transaction:
        return jsonify(error='Transaction not found'), 500

    transaction_dict = row2dict(transaction)
    transaction_dict['pieces'] = []
    for piece in transaction.pieces:
        piece_dict = row2dict(piece)
        piece_dict['product'] = row2dict(piece.product)
        transaction_dict['pieces'].append(piece_dict)

    return jsonify(transaction=transaction_dict)
