"""transaction.py - Controller calls for transaction."""
from brainwave import db
from brainwave.models import Transaction
from brainwave.controllers.transaction_piece import TransactionPieceController
from brainwave.controllers.product import ProductController


class TransactionController:
    class UnknownError(Exception):
        def __init__(self):
            self.error = 'An unexpected error occurred.'

    class MissingCredit(Exception):
        def __init__(self):
            self.error = 'The customer does not have enough credit!' + \
                         ' Transaction cancelled.'

    class BadQuantity(Exception):
        def __init__(self):
            self.error = 'The provided quantity is not valid.'

    class BadProduct(Exception):
        def __init__(self):
            self.error = 'One of the selected products does not exist.'

    @staticmethod
    def create(ta_dict):
        # Temporarily set assoc_id to 1, should be changed later
        transaction = Transaction.new_dict({'assoc_id': '1',
                                            'cust_id': ta_dict['customer_id'],
                                            'pay_type': ta_dict['pay_type'],
                                            'status': 'pending',
                                            'action': ta_dict['action']})

        if not transaction:
            raise TransactionController.UnknownError()

        db.session.add(transaction)
        db.session.commit()

        # Create individual records for each individual "transaction_piece"
        for piece in ta_dict['entries']:
            if piece['quantity'] < 0:
                raise TransactionController.BadQuantity()
            # Add transaction_id to the piece
            piece['transaction_id'] = transaction.id

            # Verify that the product exists (and use it to get the price)
            product = ProductController.get(piece['product_id'])
            if not product:
                raise TransactionController.BadProduct()

            piece['price'] = product.price * piece['quantity']

            # Create a new transaction piece
            transaction_piece = TransactionPieceController.create(piece)
            if not transaction_piece:
                raise TransactionController.UnknownError()

        # Finally, update the status of the transaction to "paid"
        TransactionController.set_status(transaction.id, 'paid')

        return transaction

    @staticmethod
    def get(transaction_id):
        """ Get a Transaction object by its id """

        return Transaction.query.get(transaction_id)

    @staticmethod
    def get_between(date_1, date_2):
        """ Get a Transaction objects between date_1 and date_2 """
        return Transaction.query.filter(Transaction.created >= date_1).\
            filter(Transaction.created <= date_2).all()

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
