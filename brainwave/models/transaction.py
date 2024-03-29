"""transaction.py - Transaction model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Transaction(db.Model, BaseEntity):
    """Transaction model."""
    __tablename__ = 'transaction'

    pay_type = db.Column(db.Enum('cash', 'pin', 'credit', name='pay_type'))
    status = db.Column(db.Enum('pending', 'paid', 'cancelled', name='status'))
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    action = db.Column(db.Enum('sell', 'refund', 'gift', name='action'))

    pieces = db.relationship('TransactionPiece', backref='transaction')

    def __init__(self, pay_type='cash', status='pending', association=None,
                 customer=None, action='sell'):
        self.pay_type = pay_type
        self.status = status
        self.association = association
        self.customer = customer
        self.action = action
