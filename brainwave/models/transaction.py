"""stock.py - Transaction model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Transaction(db.Model, BaseEntity):
    """Transaction model."""
    __tablename__ = 'transaction'
    
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    paid_by = db.Column(db.Enum('cash', 'pin', name='paid_by'))

    def __init__(self, assoc_id=None):
        self.assoc_id = assoc_id
