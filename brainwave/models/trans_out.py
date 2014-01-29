"""trans_out.py - TransOut model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class TransOut(db.Model, BaseEntity):
    """"The transaction out Model"""
    __tablename__ = 'trans_out'

    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))

    def __init__(self, price=None, quantity=None, stock=None):
        self.price = price
        self.quantity = quantity
        self.stock = stock
