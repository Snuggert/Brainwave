"""stock.py - Stock model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Stock(db.Model, BaseEntity):
    """Stock model."""
    __tablename__ = 'stock'

    name = db.Column(db.String(256))
    quantity = db.Column(db.Integer)
    direct = db.Column(db.Boolean)

    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    products = db.relationship('Product', backref='stock')
    transactions_in = db.relationship('TransIn', backref='stock')

    def __init__(self, name=None, direct=True, association=None):
        self.name = name
        self.quantity = 0
        self.direct = direct
        self.association = association
