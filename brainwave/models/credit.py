"""credit.py - Credit model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db


class Credit(db.Model, BaseEntity):
    """Credit model."""
    __tablename__ = 'credit'

    credit = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    association_id = db.Column(db.Integer, db.ForeignKey('association.id'))

    customer = db.relationship('Customer', backref=db.backref('credits',
                                                              lazy='dynamic'))
    association = db.relationship('Association',
                                  backref=db.backref('credits',
                                                     lazy='dynamic'))

    def __init__(self, credit=0.0, customer=None, association=None):
        """Initialize a credit."""
        self.credit = credit
        self.customer = customer
        self.association = association
