from brainwave import db
from brainwave.utils import BaseEntity

class ProductCategory(db.Model, BaseEntity):
    __tablename__ = 'product_category'

    prints = ['id', 'name']

    name = db.Column(db.String(256))

    products = db.relationship('Product', backref='prduct_category')

    def __init__(self, name):
        self.name = name