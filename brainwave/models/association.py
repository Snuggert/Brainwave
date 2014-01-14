"""association.py - Association model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db
from sqlalchemy import Integer, ForeignKey


class Association(db.Model, BaseEntity):
    """Association model."""
    __tablename__ = 'association'

    name = db.Column(db.String(256))
    products = db.relationship('Product', backref='association')
    stocks = db.relationship('Stock', backref='association')
    user_id = db.Column(Integer, ForeignKey('user.id'))

    def __init__(self, name='', user_id=''):
        """Initialize the association."""
        self.name = name
        self.user_id = user_id
