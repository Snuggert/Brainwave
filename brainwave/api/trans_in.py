"""trans_in.py - API calls for transaction-in."""
from brainwave import db
from brainwave.models import TransIn

class TransInAPI:
    """The API for transaction-in manipulation."""

    @staticmethod
    def create(trans_in_dict):
        trans_in = TransIn.new_dict(trans_in_dict)
        print trans_in_dict['stock_id']
        db.session.add(stock)
        db.session.commit()

        return stock