"""customer.py - Customer model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db


class Customer(db.Model, BaseEntity):
    """Customer model."""
    __tablename__ = 'customer'

    name = db.Column(db.String(256))

    def __init__(self, name=''):
        """Initialize a customer."""
        self.name = name
