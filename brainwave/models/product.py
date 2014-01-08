"""product.py - Product model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class Product(db.Model, BaseEntity):
    """Product model."""
    __tablename__ = 'product'

    prints = ['id', 'name']

    active = db.Column(db.Boolean)
    name = db.Column(db.String(256))
    shortname = db.Column(db.String(32))
    price = db.Column(db.Float)
    # Probably in milliliters?
    volume = db.Column(db.Integer)
    # Percentage in Floats???
    loss = db.Column(db.Float)

    product_category_id = db.Column(db.Integer,
                                    db.ForeignKey('product_category.id'))

    def __init__(self, name='', shortname='', price=None, volume=None,
                 product_category=None):
        self.active = False
        self.name = name
        self.shortname = shortname
        self.price = price
        self.volume = volume
        product_category = product_category
