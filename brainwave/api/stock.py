"""stock.py - API calls for stock."""
from .brainwave import db
from .brainwave.models.stock import Stock

class StockAPI:
    """The API for stock manipulation."""

    @staticmethod
    def create(stock_dict):
        stock = Stock.new_dict(stock_dict)

        db.session.add(stock)
        db.session.commit()

        return stock

    @staticmethod
    def add(item, quantity):
        """ Add a certain quantity to stock. Use negative to remove items from
        stock
        """
        item.quantity = item.quantity + quantity
        
        db.session.commit()

        return item

    @staticmethod
    def get(stock_id):
        """ Get a stock object bij its id """

        return Stock.query.get(stock_id).first()

    @staticmethod
    def get_all():
        """ Get all stock items """

        return Stock.query.all()

    @staticmethod
    def delete(item):
        """ Delete stock item """
        db.session.delete(item)
        db.session.commit()
        return
