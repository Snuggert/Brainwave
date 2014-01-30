"""association.py - Association model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db
from sqlalchemy import Integer, ForeignKey


class Association(db.Model, BaseEntity):
    """Association model."""
    __tablename__ = 'association'

    name = db.Column(db.String(256))
    user_id = db.Column(Integer, ForeignKey('user.id'))
    minimum_credit = db.Column(db.Float)
    cash_counter = db.Column(db.Float)

    products = db.relationship('Product', backref='association')
    stocks = db.relationship('Stock', backref='association')
    transactions = db.relationship('Transaction', backref='association')

    def __init__(self, name='', user_id='', minimum_credit=0, cash_counter=0):
        """Initialize the association."""
        self.name = name
        self.user_id = user_id
        self.minimum_credit = minimum_credit
        self.cash_counter = cash_counter
