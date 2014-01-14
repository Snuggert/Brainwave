"""transaction.py - Controller calls for transaction."""
from brainwave import db
from brainwave.models import Transaction
from brainwave.controllers.transaction_piece import TransactionPieceController
# Change product api to controller when the switch has been made
from brainwave.controllers.product import ProductController


class TransactionController:
    @staticmethod
    def create(dict):
        # Temporarily set assoc_id to 1, should be changed later
        transaction = Transaction.new_dict({'assoc_id': '1',
                                            'pay_type': dict['pay_type'],
                                            'status': 'pending'})
        if not transaction:
            return False

        db.session.add(transaction)
        db.session.commit()

        # Create individual records for each individual "transaction_piece"
        for piece in dict['items']:
            # Add transaction_id to the piece
            piece['transaction_id'] = transaction.id
            # Verify that the product exists (and use it to get the price)
            product = ProductController.get(piece['product_id'])
            if not product:
                return False
            piece['price'] = product.price

            transaction_piece = TransactionPieceController.create(piece)
            if not transaction_piece:
                return False

        # Finally, update the status of the transaction to "paid"
        transaction.status = 'paid'
        db.session.commit()

        return transaction

    @staticmethod
    def get(transaction_id):
        """ Get a Transaction object by its id """

        return Transaction.query.get(transaction_id)

    @staticmethod
    def get_all():
        """ Get all Transaction objects """

        return Transaction.query.all()
