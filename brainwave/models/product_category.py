"""product_category.py - ProductCategory model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class ProductCategory(db.Model, BaseEntity):
    """ProductCategory model."""
    __tablename__ = 'product_category'

    prints = ['id', 'name']

    name = db.Column(db.String(256))

    products = db.relationship('Product', backref='product_category')

    def __init__(self, name):
        self.name = name
