"""customer.py - Customer model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db

customer_association = db.Table('customer_association',
                                db.Column('id', db.Integer, primary_key=True),
                                db.Column('customer_id', db.Integer,
                                          db.ForeignKey('customer.id')),
                                db.Column('association_id', db.Integer,
                                          db.ForeignKey('association.id')))


class Customer(db.Model, BaseEntity):
    """Customer model."""
    __tablename__ = 'customer'

    name = db.Column(db.String(256))

    associations = db.relationship('Association',
                                   secondary=customer_association,
                                   backref=db.backref('customers',
                                                      lazy='dynamic'),
                                   lazy='dynamic')

    def __init__(self, name=''):
        """Initialize a customer."""
        self.name = name
