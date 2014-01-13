"""association.py - Association model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db


class Association(db.Model, BaseEntity):
    """Association model."""
    __tablename__ = 'association'

    name = db.Column(db.String(256))
    products = db.relationship('Product', backref='association')
    stocks = db.relationship('Stock', backref='association')

    def __init__(self, name=''):
        """Initialize the association."""
        self.name = name
