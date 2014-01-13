"""stock.py - Stock model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Stock(db.Model, BaseEntity):
    """Stock model."""
    __tablename__ = 'stock'

    name = db.Column(db.String(256))
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))
    quantity = db.Column(db.Integer)

    products = db.relationship('Product', backref='stock')
    transactions = db.relationship('TransIn', backref='stock')

    def __init__(self, name=None, quantity=0, association=None):
        self.name = name
        self.association = association
        self.quantity = quantity
