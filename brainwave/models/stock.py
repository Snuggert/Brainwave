"""stock.py - Stock model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Stock(db.Model, BaseEntity):
    """Stock model."""
    __tablename__ = 'stock'

    prints = ['id', 'stock']

    stock = db.Column(db.Integer)
    stock_type = db.Column(db.Integer)

    def __init__(self, stock=None, stock_type=None):
        self.stock = stock
        self.stock_type = stock_type
