"""stock.py - Stock model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Stock(db.Model, BaseEntity):
    """Stock model."""
    __tablename__ = 'stock'

    quantity = db.Column(db.Integer)
    name = db.Column(db.String(256))

    def __init__(self, quantity=0, name=None):
        self.quantity = quantity
        self.name = name