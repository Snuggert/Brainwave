"""transaction.py - Transaction model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Transaction(db.Model, BaseEntity):
    """Transaction model."""
    __tablename__ = 'transaction'
    
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    pay_type = db.Column(db.Enum('cash', 'pin', name='pay_type'))

    status = db.Column(db.Enum('pending', 'paid', 'cancelled', name='status'))

    transactions = db.relationship('TransactionPiece', backref='transaction')

    def __init__(self, assoc_id=None, pay_type='cash', status='cancelled'):
        self.assoc_id = assoc_id
        self.pay_type = pay_type
        self.status = status
