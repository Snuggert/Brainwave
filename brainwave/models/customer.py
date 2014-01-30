"""customer.py - Customer model."""
from werkzeug.security import generate_password_hash
from brainwave.utils.base_model import BaseEntity
from brainwave.models import User
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    associations = db.relationship('Association',
                                   secondary=customer_association,
                                   backref=db.backref('customers',
                                                      lazy='dynamic'),
                                   lazy='dynamic')

    def __init__(self, name='', password='password', email='default@something.com', username=''):
        """Initialize a customer."""
        if username == "":
            username = name
        user = User(username, generate_password_hash(password), email, 1)
        db.session.add(user)
        db.session.commit()
        self.name = name
        self.user = user
