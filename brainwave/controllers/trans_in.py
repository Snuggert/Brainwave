"""trans_in.py - Controller calls for transaction-in."""
from brainwave import db
from brainwave.models import TransIn, Stock
from .stock import StockController
from sqlalchemy import func


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
    def remove_from_stock(global_product_id):
        """ Remove an item from the stock """
        product = TransIn.query.filter_by(stock_id=global_product_id,
                                          in_stock=True).first()

        if not product:
            return None

        product.in_stock = False

        db.session.commit()

        return True

    @staticmethod
    def get_all():
        """Get all trans_in items."""
        return TransIn.query.filter_by(in_stock=True).all()

    @staticmethod
    def get_all_merged(query=None):
        """ Merge all the transactions to get a stock overview """
        if query:
            all_stock = StockController.get_all_from(query)
        else:
            all_stock = StockController.get_all()

        for stock in all_stock:
            # Get the sum of all the transactions
            stock.volumesum = TransIn.query.with_entities(func.sum
                                                          (TransIn.volume).
                                                          label('volumesum')).\
                filter(TransIn.stock_id == stock.id,
                       TransIn.in_stock).all()

            # Get the sum of all the transactions prices
            stock.pricesum = TransIn.query.with_entities(func.sum
                                                         (TransIn.price).
                                                         label('pricesum')).\
                filter(TransIn.stock_id == stock.id,
                       TransIn.in_stock).all()

            # Get the amount of tranction items
            stock.amount = TransIn.query.with_entities(func.count
                                                       (TransIn.id).
                                                       label('amount')).\
                filter(TransIn.stock_id == stock.id,
                       TransIn.in_stock).all()

        return all_stock

    @staticmethod
    def delete(item):
        """Delete trans_in item."""
        db.session.delete(item)
        db.session.commit()

        return
