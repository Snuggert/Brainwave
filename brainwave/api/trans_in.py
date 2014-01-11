"""trans_in.py - API calls for transaction-in."""
from brainwave import db
from brainwave.models import TransIn
from brainwave.utils import row2dict
from .stock import StockAPI


class TransInAPI:
    """The API for transaction-in manipulation."""
    @staticmethod
    def create(trans_in_dict):
        trans_in_dict['stock'] = StockAPI.get(trans_in_dict['stock_id'])
        trans_in = TransIn.new_dict(trans_in_dict)
        StockAPI.add(StockAPI.get(trans_in_dict['stock_id']),
                     trans_in_dict['volume'])
        db.session.add(trans_in)
        db.session.commit()

        return row2dict(trans_in)

    @staticmethod
    def get(trans_in_id):
        """ Get a transaction-in object by its id """
        trans_in = TransIn.query.get(trans_in_id)
        if trans_in is None:
            return None
        return row2dict(trans_in)

    @staticmethod
    def get_all():
        """ Get all trans_in items """
        transactions = TransIn.query.all()
        transactions_with = []
        for item in transactions:
            dictitem = row2dict(item)
            dictitem['stock'] = row2dict(StockAPI.get(dictitem['stock_id']))
            transactions_with.append(dictitem)
        return transactions_with

    @staticmethod
    def delete(item):
        """ Delete trans_in item """
        if type(item) is dict:
            item = TransIn.by_id(item['id'])
        db.session.delete(item)
        db.session.commit()
        return