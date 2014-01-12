"""association.py - API calls for association."""
from werkzeug.security import generate_password_hash, check_password_hash
from brainwave.models.association import Association
from brainwave.utils import row2dict
from brainwave import db


class AssociationAPI:
    """The API for association manipulation."""
    class NoPassword(Exception):
        """Exception for when a password is missing."""
        def __init__(self):
            """Initialize with a standard message."""
            self.error = 'No password given'

    @staticmethod
    def create(association_dict):
        """Create a new association."""
        password = association_dict.pop('password', None)
        if not password:
            raise AssociationAPI.NoPassword()

        association = Association.new_dict(association_dict)

        pw_hash = generate_password_hash(password)
        association.pw_hash = pw_hash

        db.session.add(association)
        db.session.commit()

        return association

    @staticmethod
    def update(association_dict):
        """Update an association."""
        password = association_dict.pop('password', None)

        association = Association.merge_dict(association_dict)

        if password:
            pw_hash = generate_password_hash(password)
            association.pw_hash = pw_hash

        db.session.add(association)
        db.session.commit()

        return association

    @staticmethod
    def delete(association):
        """Delete an association."""
        db.session.delete(association)
        db.session.commit()

    @staticmethod
    def get(association_id):
        """Get an association by its id."""
        return Association.query.get(association_id)

    @staticmethod
    def get_all():
        """Get all associations."""
        return Association.query.all()

    @staticmethod
    def check_password(association, password):
        """Check whether the given password is correct."""
        return check_password_hash(association.pw_hash, password)
