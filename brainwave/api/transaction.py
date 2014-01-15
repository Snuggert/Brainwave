"""transaction.py - Transaction for user."""
from flask import Blueprint, jsonify, request
from brainwave.controllers.transaction import TransactionController

transaction_api = Blueprint('transaction_api', __name__,
                            url_prefix='/api/transaction')

# Dictionary format example:
# {
#    "pay_type":"cash",
#    "items":[
#       {
#          "product_id":"1",
#          "action":"sell"
#       },
#       {
#          "product_id":"2",
#          "action":"sell"
#       }
#    ]
# }
#
# pay_type can be either cash or pin (credit should become option 3, later)
# action can be sell, refund or gift
@transaction_api.route('/new', methods=['POST'])
def create():
    """Create a new transaction."""
    dict = request.json

    # Note that the TransactionController creates records for both the
    # Transaction table as the TransactionPiece table.
    transaction = TransactionController.create(dict)

    if not transaction:
        return jsonify(status='failed', error="Could not sell items."), 500

    return jsonify(status='success')