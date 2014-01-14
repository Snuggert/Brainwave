"""trans_in.py - Controller calls for transaction-in."""
from brainwave import db
from brainwave.models import TransIn
from .stock import StockController


class TransInController:
    """The Controller for transaction-in manipulation."""
    @staticmethod
    def create(trans_in_dict):
        trans_in = TransIn.new_dict(trans_in_dict)

        db.session.add(trans_in)
        db.session.commit()

        StockController.add(trans_in.stock, trans_in.volume)

        return trans_in

    @staticmethod
    def get(trans_in_id):
        """Get a transaction-in object by its id."""
        return TransIn.query.get(trans_in_id)

    @staticmethod
    def get_all():
        """Get all trans_in items."""
        return TransIn.query.all()

    @staticmethod
    def delete(item):
        """Delete trans_in item."""
        db.session.delete(item)
        db.session.commit()

        return
