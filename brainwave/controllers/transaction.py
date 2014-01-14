"""transaction.py - Controller calls for transaction."""
from brainwave import db
import difflib
from brainwave.models import Transaction


class TransactionController:
    @staticmethod
    def create(dict):
        transaction = Transaction.new_dict(dict)

        db.session.add(transaction)
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
