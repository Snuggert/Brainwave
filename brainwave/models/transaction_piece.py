"""transaction_piece.py - TransactionPiece model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class TransactionPiece(db.Model, BaseEntity):
    """TransactionPiece model."""
    __tablename__ = 'transaction_piece'

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    price = db.Column(db.Float)

    action = db.Column(db.Enum('sell', 'refund', 'gift', name='action'))

    def __init__(self, transaction_id=None, product_id=None, price=None,
                 action='sell'):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.price = price
        self.action = action
