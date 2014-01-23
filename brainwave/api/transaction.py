"""transaction.py - Transaction for user."""
from flask import Blueprint, jsonify, request
from brainwave.controllers.transaction import TransactionController
from brainwave.controllers.authentication import Authentication
from brainwave.models import User

transaction_api = Blueprint('transaction_api', __name__,
                            url_prefix='/api/transaction')


# Dictionary format example:
# {
#    "pay_type":"cash",
#    "items":[
#       {
#          "product_id":"1",
#          "quantity": "7",
#          "action":"sell"
#       },
#       {
#          "product_id":"2",
#          "quantity": "100",
#          "action":"sell"
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
    dict = request.json
    print dict
    # Note that the TransactionController creates records for both the
    # Transaction table as the TransactionPiece table.
    transaction = TransactionController.create(dict)

    if not transaction:
        return jsonify(status='failed', error="Could not sell items."), 500

    return jsonify(status='success')
