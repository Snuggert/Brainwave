"""stock.py - API calls for stock."""
from brainwave import db
from brainwave.utils import row2dict
from brainwave.models import Stock


class StockAPI:
    """The API for stock manipulation."""
    @staticmethod
    def create(stock_dict):
        stock = Stock.new_dict(stock_dict)

        db.session.add(stock)
        db.session.commit()

        return row2dict(stock)

    @staticmethod
    def add(item, quantity):
        """ Add a certain quantity to stock. Use negative to remove items from
        stock
        """
        if type(item) is dict:
            item['quantity'] = item['quantity'] + quantity
            item = Stock.merge_dict(item)
        else:
            item.quantity = item.quantity + quantity

        db.session.add(item)
        db.session.commit()

        return row2dict(item)

    @staticmethod
    def get(stock_id):
        """ Get a stock object by its id """
        stock = Stock.query.get(stock_id)
        if stock is None:
            return None
        else:
            return row2dict(stock)

    @staticmethod
    def get_all():
        """ Get all stock items """
        return Stock.query.all()

    @staticmethod
    def delete(item):
        """ Delete stock item """
        if type(item) is dict:
            item = Stock.by_id(item['id'])
        db.session.delete(item)
        db.session.commit()
        return