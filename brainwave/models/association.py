"""association.py - Association model."""
from brainwave.utils.base_model import BaseEntity
from brainwave import db


class Association(db.Model, BaseEntity):
    """Association model."""
    __tablename__ = 'association'

    login_name = db.Column(db.String(256))
    pw_hash = db.Column(db.String(66))

    name = db.Column(db.String(256))

    def __init__(self, login_name='', pw_hash='', name=''):
        """Initialize the association."""
        self.login_name = login_name
        self.pw_hash = pw_hash
        self.name = name
