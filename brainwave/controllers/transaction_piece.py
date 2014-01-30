"""transaction_piece.py - Controller calls for TransactionPieces."""
from brainwave import db
from brainwave.models import TransactionPiece, Product
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import time


class TransactionPieceController:
    @staticmethod
    def create(dict):
        transaction_piece = TransactionPiece.new_dict(dict)

        db.session.add(transaction_piece)
        db.session.commit()

        return transaction_piece

    @staticmethod
    def get_all_from(trans_id):
        """ Get all TransactionPiece objects by their shared transaction_id """

        return TransactionPiece.query.filter(transaction_id=trans_id).all()

    @staticmethod
    def get_all_merged(from_date='1-1-1970',
                       to_date=time.strftime("%d-%m-%Y")):
        """ Merge all the merged transactions to get a sales overview """

        # Convert date strings to datetime objects
        from_date = datetime.strptime(from_date, '%d-%m-%Y')
        to_date = datetime.strptime(to_date, '%d-%m-%Y') +\
            timedelta(days=1)

        # Retreive all products
        products = Product.query.all()

        for product in products:
            # Get the sum of all the transactions
            product.quantitysum = TransactionPiece.query.\
                with_entities(func.sum(TransactionPiece.quantity).
                              label('quantitysum')).\
                filter(TransactionPiece.product_id == product.id,
                       and_(TransactionPiece.created >= from_date,
                            TransactionPiece.created <= to_date)
                       ).all()

            # Get the sum of all the transactions prices
            product.pricesum = TransactionPiece.query.\
                with_entities(func.sum(TransactionPiece.price).
                              label('pricesum')).\
                filter(TransactionPiece.product_id == product.id,
                       and_(TransactionPiece.created >= from_date,
                            TransactionPiece.created <= to_date)
                       ).all()

            # Get the amount of tranction items
            product.amount = TransactionPiece.query.\
                with_entities(func.count
                              (TransactionPiece.id).label('amount')).\
                filter(TransactionPiece.product_id == product.id,
                       and_(TransactionPiece.created >= from_date,
                            TransactionPiece.created <= to_date)
                       ).all()

        return products
