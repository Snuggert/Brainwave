"""product_category.py - ProductCategory model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class ProductCategory(db.Model, BaseEntity):
    """ProductCategory model."""
    __tablename__ = 'product_category'

    prints = ['id', 'name']

    name = db.Column(db.String(256))
    color = db.Column(db.String(6))
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    products = db.relationship('Product', backref='product_category')

    def __init__(self, name='', color='FFFFFF', assoc_id=''):
        self.name = name
        self.color = color
        self.assoc_id = assoc_id
