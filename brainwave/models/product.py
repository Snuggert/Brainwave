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
    quantity = db.Column(db.Integer)
    unit = db.Column(db.Enum('cL', 'amount', name='unit'))
    direct = db.Column(db.Boolean)

    product_category_id = db.Column(db.Integer,
                                    db.ForeignKey('product_category.id'))
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    assoc_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    sold_pieces = db.relationship('TransactionPiece', backref='product')

    def __init__(self, name='', shortname='', price=None, quantity=None,
                 unit='cL', direct=True, product_category=None, stock=None,
                 association=None):
        self.active = False
        self.name = name
        self.shortname = shortname
        self.price = price
        self.quantity = quantity
        self.unit = unit
        self.direct = direct
        self.product_category = product_category
        self.stock = stock
        self.association = association
