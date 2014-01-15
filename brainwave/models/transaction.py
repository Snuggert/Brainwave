"""transaction.py - Transaction model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Transaction(db.Model, BaseEntity):
    """Transaction model."""
    __tablename__ = 'transaction'

    trans_in = db.Column(db.Boolean)
    pay_type = db.Column(db.Enum('cash', 'pin', name='pay_type'))
    status = db.Column(db.Enum('pending', 'paid', 'cancelled', name='status'))
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    pieces = db.relationship('TransactionPiece', backref='transaction')

    def __init__(self, pay_type='cash', status='pending', association=None,
                 trans_in=False):
        self.pay_type = pay_type
        self.status = status
        self.association = association
        self.trans_in = trans_in
