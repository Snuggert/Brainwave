"""transaction_piece.py - TransactionPiece model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class TransactionPiece(db.Model, BaseEntity):
    """TransactionPiece model."""
    __tablename__ = 'transaction_piece'

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    quantity = db.Column(db.Integer)

    price = db.Column(db.Float)

    def __init__(self, transaction=None, product=None, quantity=None,
                 price=None):
        self.transaction = transaction
        self.product = product
        self.quantity = quantity
        self.price = price
