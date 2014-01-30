"""transaction.py - Transaction for user."""
from flask import Blueprint, jsonify, request
from brainwave.utils import row2dict
from brainwave.controllers.transaction import TransactionController
from brainwave.controllers.transaction_piece import TransactionPieceController
from brainwave.controllers.authentication import Authentication
from brainwave.models import User, Transaction
import time

transaction_api = Blueprint('transaction_api', __name__,
                            url_prefix='/api/transaction')


# Dictionary format example:
# {
#    "pay_type":"cash",
#    "action":"sell",
#    "entries":[
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
    try:
        TransactionController.create(transaction_dict)
    except TransactionController.MissingCredit as e:
        return jsonify(status='error', error=e.error), 500
    except TransactionController.NoAssociation as e:
        return jsonify(status='error', error=e.error), 500
    except TransactionController.BadQuantity as e:
        return jsonify(status='error', error=e.error), 500
    except TransactionController.BadProduct as e:
        return jsonify(status='error', error=e.error), 500
    except TransactionController.UnknownError as e:
        return jsonify(status='error', error=e.error), 500
    except TransactionController.NoCustomerSelected as e:
        return jsonify(status='error', error=e.error), 500

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


@transaction_api.route('/sales', methods=['GET'])
@transaction_api.route('/sales/<string:from_date>/<string:to_date>',
                       methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_all_merged(from_date='1-1-2013 00:00',
                   to_date=time.strftime("%d-%m-%Y %H:%M")):
    """Get all sales transaction pieces merged."""
    transactions = TransactionPieceController.get_all_merged(from_date,
                                                             to_date)

    transaction_dict = dict()
    for transaction in transactions:
        product_sales = dict()
        product_sales['price'] = transaction.price
        product_sales['amount'] = transaction.amount[0][0]
        product_sales['amount'] = transaction.amount[0][0]
        product_sales['pricesum'] = transaction.pricesum[0][0]
        product_sales['quantitysum'] = transaction.quantitysum[0][0]
        product_sales['name'] = transaction.name
        transaction_dict[transaction.name] = product_sales

    return jsonify(transaction=transaction_dict)
