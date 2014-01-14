"""transaction.py - Controller calls for transaction."""
from brainwave import db
from brainwave.models import Transaction
from brainwave.controllers.transaction_piece import TransactionPieceController
# Change product api to controller when the switch has been made
from brainwave.controllers.product import ProductController


class TransactionController:
    @staticmethod
    def create(dict):

        # Create a new transaction object first. Note that it is not yet being
        # added to the database. This only happens when all the pieces have been
        # added successfully.

        # Temporarily set assoc_id to 1, should be changed later
        transaction = Transaction.new_dict({'assoc_id':'1',
                                            'pay_type':dict['pay_type']})

        if not transaction:
            return False

        # Create individual records for each individual "transaction_piece"
        for piece in dict['items']:
            print piece
            # Add transaction_id to the piece
            piece['transaction_id'] = transaction.id
            # Verify that the product exists (and use it to get the price)
            product = ProductAPI.get(piece['product_id'])
            if not product:
                return False
            piece['price'] = product.price

            transaction_piece = TransactionPieceController.create(piece)
            if not transaction_piece:
                return False
            else:
                print transaction_piece.id

        # Now that all pieces were added successfully, add the transaction
        # record itself.
        db.session.add(transaction)
        db.session.commit()

        print transaction.id

        return transaction

    @staticmethod
    def get(transaction_id):
        """ Get a Transaction object by its id """

        return Transaction.query.get(transaction_id)

    @staticmethod
    def get_all():
        """ Get all Transaction objects """

        return Transaction.query.all()
