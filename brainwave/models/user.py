"""user.py - User model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db


class User(BaseEntity):
    """User model."""
    __tablename__ = 'user'

    username = db.Column(db.String(256))
    pw_hash = db.Column(db.String(66))

    name = db.Column(db.String(256))

    def __init__(self, username='', pw_hash='', name=''):
        """Initialize the user."""
        self.username = username
        self.pw_hash = pw_hash
        self.name = name
