"""transaction.py - Controller calls for transaction."""
from brainwave import db
from brainwave.models import Transaction
from brainwave.controllers.transaction_piece import TransactionPieceController
from brainwave.controllers.product import ProductController


class TransactionController:
    @staticmethod
    def create(dict):
        # Temporarily set assoc_id to 1, should be changed later
        transaction = Transaction.new_dict({'assoc_id': '1',
                                            'pay_type': 'cash',
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
        TransactionController.set_status(transaction.id, 'paid')

        return transaction

    @staticmethod
    def get(transaction_id):
        """ Get a Transaction object by its id """

        return Transaction.query.get(transaction_id)

    @staticmethod
    def set_status(transaction_id, status):
        """ Set the status of a transaction """
        Transaction.query.filter_by(id=transaction_id) \
                         .update(dict(status=status))
        db.session.commit()

    @staticmethod
    def get_all():
        """ Get all Transaction objects """

        return Transaction.query.all()
