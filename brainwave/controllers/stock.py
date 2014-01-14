"""stock.py - Controller calls for stock."""
from brainwave import db
import difflib
from brainwave.models import Stock


class StockController:
    """The Controller for stock manipulation."""

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

        db.session.add(item)
        db.session.commit()

        return item

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
