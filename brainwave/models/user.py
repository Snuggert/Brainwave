"""user.py - User model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db

ROLE_NONE = 0
ROLE_CUSTOMER = 1
ROLE_BAR_TEAM = 2
ROLE_ASSOCIATION = 4
ROLE_ADMIN = 8


class User(db.Model, BaseEntity):
    """User model."""
    __tablename__ = 'user'

    login_name = db.Column(db.String(256))
    pw_hash = db.Column(db.String(66))
    email = db.Column(db.String(120))
    role = db.Column(db.Integer())

    def __init__(self, login_name='', pw_hash='', email='', role=ROLE_NONE):
        """Initialize the User."""
        self.login_name = login_name
        self.pw_hash = pw_hash
        self.email = email
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.login_name)
