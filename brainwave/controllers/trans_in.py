"""trans_in.py - Controller calls for transaction-in."""
from brainwave import db
from brainwave.models import TransIn, User
from flask import session


class TransInController:
    """The Controller for transaction-in manipulation."""
    @staticmethod
    def create(trans_in_dict):
        trans_in = TransIn.new_dict(trans_in_dict)
        db.session.add(trans_in)
        db.session.commit()

        return trans_in

    @staticmethod
    def get(trans_in_id):
        """Get a transaction-in object by its id."""
        return TransIn.query.get(trans_in_id)

    #     #Get the first positive transaction.
    #     trans_in = TransIn.query.filter_by(stock_id=global_product_id,
    #                                        in_stock=True).\
    #         filter(TransIn.quantity > 0).first()

    #     #Create a new transaction when no transaction is found.
    #     if not trans_in:
    #     trans_in = TransIn.query.filter_by(stock_id=global_product_id,
    #                                          ).order_by(TransIn.id.desc()).\
    #             filter(TransIn.quantity > 0).first()

    #         stock = Stock.query.filter_by(id=trans_in.stock_id).first()
    #    negative_transaction = TransIn(-trans_in.price, -trans_in.quantity,
    #                                        stock=stock)
    #         negative_transaction.in_stock = True
    #         db.session.add(negative_transaction)
    #        db.session.commit()
    #         return None
    #    trans_in.in_stock = False
    #     db.session.commit()
    #     return True

    @staticmethod
    def put_back_in_stock(global_product_id):
        """ Undo a remove from stock action """
        product = TransIn.query.filter_by(stock_id=global_product_id,
                                          in_stock=False).last()

        if not product:
            return None

        product.in_stock = True

        db.session.commit()

        return True

    @staticmethod
    def get_all():
        # """Get all trans_in items."""
        # if session['user_role'] >= User.ROLE_ADMIN:
        #     return TransIn.query.all()
        # else:
        #     return TransIn.query.all()

        # TransIn.query.filter(TransIn.stock_id.assoc_id == assoc_id).all()
        return TransIn.query.all()

    # @staticmethod
    # def get_all_merged(query=None):
    #     """ Merge all the transactions to get a stock overview """
    #     if query:
    #         all_stock = StockController.get_all_from(query)
    #     else:
    #         all_stock = StockController.get_all()

    #     for stock in all_stock:
    #         # Get the sum of all the transactions
    #         stock.quantitysum = \
    #                 TransIn.query.with_entities(func.sum(TransIn.quantity).
    #                                             label('quantitysum')).\
    #             filter(TransIn.stock_id == stock.id,
    #                    TransIn.in_stock).all()

    #         # Get the sum of all the transactions prices
    #         stock.pricesum = TransIn.query.with_entities(func.sum
    #                                                      (TransIn.price).
    #                                                      label('pricesum')).\
    #             filter(TransIn.stock_id == stock.id,
    #                    TransIn.in_stock).all()

    #         # Get the amount of tranction items
    #         stock.amount = TransIn.query.with_entities(func.count
    #                                                    (TransIn.id).
    #                                                    label('amount')).\
    #             filter(TransIn.stock_id == stock.id,
    #                    TransIn.in_stock).all()

    #     return all_stock

    @staticmethod
    def delete(item):
        """Delete trans_in item."""
        db.session.delete(item)
        db.session.commit()

        return
