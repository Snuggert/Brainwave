"""user.py - User model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db


class User(db.Model, BaseEntity):
    """Association model."""
    __tablename__ = 'user'

    login_name = db.Column(db.String(256))
    pw_hash = db.Column(db.String(66))
    email = db.Column(db.String(120))

    def __init__(self, login_name='', pw_hash='', email=''):
        """Initialize the association."""
        self.login_name = login_name
        self.pw_hash = pw_hash
        self.email = email
