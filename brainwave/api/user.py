"""user.py - API calls for user."""
from werkzeug.security import generate_password_hash, check_password_hash
from brainwave.models.user import User
from brainwave.utils import row2dict
from brainwave import db


class UserAPI:
    """The API for user manipulation."""
    class NoPassword(Exception):
        """Exception for when a password is missing."""
        def __init__(self):
            """Initialize with a standard message."""
            self.error = 'No password given'

    @staticmethod
    def create(user_dict):
        """Create a new user."""
        password = user_dict.pop('password', None)
        if not password:
            raise UserAPI.NoPassword()

        user = User.new_dict(user_dict)

        pw_hash = generate_password_hash(password)
        user.pw_hash = pw_hash

        db.session.add(user)
        db.session.commit()

        return row2dict(user)

    @staticmethod
    def update(user_dict):
        """Update a user."""
        password = user_dict.pop('password', None)

        user = User.merge_dict(user_dict)

        if password:
            pw_hash = generate_password_hash(password)
            user.pw_hash = pw_hash

        db.session.add(user)
        db.session.commit()

        return row2dict(user)

    @staticmethod
    def delete(item):
        """Delete a user."""
        if type(item) is dict:
            item = User.by_id(item['id'])
        db.session.delete(item)
        db.session.commit()
        return

    @staticmethod
    def get(user_id):
        """Get a user by its id."""
        user = User.query.get(user_id)
        if user is None:
            return None
        return row2dict(user)

    @staticmethod
    def get_all():
        """Get all users."""
        users = User.query.all()
        return_users = []
        for item in users:
            return_users.append(row2dict(item))
        return return_users

    @staticmethod
    def check_password(user, password):
        """Check whether the given password is correct."""
        return check_password_hash(user['pw_hash'], password)
