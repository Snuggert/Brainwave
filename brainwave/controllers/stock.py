"""stock.py - Controller calls for stock."""
from brainwave import db
import difflib
from brainwave.models import Stock
# from brainwave.controllers import TransInController


class StockController:
    """The Controller for stock manipulation."""
    class NoNameGiven(Exception):
        """Exception for when no name is given for a stock."""
        def __init__(self):
            self.error = 'No name was given for the stock'

    @staticmethod
    def add(stock, quantity):
        stock.quantity = stock.quantity + quantity
        db.session.add(stock)
        db.session.commit()

    @staticmethod
    def update(stock_dict):
        print stock_dict
        stock = Stock.merge_dict(stock_dict)
        if not stock.name:
            raise StockController.NoNameGiven()
        db.session.add(stock)
        db.session.commit()

        return stock

    @staticmethod
    def remove(stock, quantity):
        stock.quantity = stock.quantity - quantity
        db.session.add(stock)
        db.session.commit()

    @staticmethod
    def create(stock_dict):
        stock = Stock.new_dict(stock_dict)

        db.session.add(stock)
        db.session.commit()

        return stock

    @staticmethod
    def get(stock_id):
        """ Get a stock object by its id """

        return Stock.query.get(stock_id)

    @staticmethod
    def get_all():
        """ Get all stock objects """

        return Stock.query.all()

    @staticmethod
    def get_all_from(query):
        """ Get all stock objects searched by query """

        stock = Stock.query.all()
        items = [item.name for item in stock]

        result_names = difflib.get_close_matches(query, items, len(items),
                                                 0.25)

        results = Stock.query.filter(Stock.name.in_(result_names)).all()

        return results

    @staticmethod
    def delete(item):
        """ Delete stock item """
        db.session.delete(item)
        db.session.commit()
        return
