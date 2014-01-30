"""stock.py - Stock model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Stock(db.Model, BaseEntity):
    """Stock model."""
    __tablename__ = 'stock'

    name = db.Column(db.String(256))
    quantity = db.Column(db.Integer)

    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    products = db.relationship('Product', backref='stock')
    transactions_in = db.relationship('TransIn', backref='stock')

    def __init__(self, name=None, association=None):
        self.name = name
        self.quantity = 0
        self.association = association
