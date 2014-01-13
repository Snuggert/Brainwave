"""user.py - Controller for user."""
from werkzeug.security import generate_password_hash, check_password_hash
from brainwave.models.user import User
from brainwave import db


class UserController:
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
            raise UserController.NoPassword()

        user = User.new_dict(user_dict)

        pw_hash = generate_password_hash(password)
        user.pw_hash = pw_hash

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def update(user_dict):
        """Update an user."""
        password = user_dict.pop('password', None)

        user = User.merge_dict(user_dict)

        if password:
            pw_hash = generate_password_hash(password)
            user.pw_hash = pw_hash

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def delete(user):
        """Delete an user."""
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def get(user_id):
        """Get an user by its id."""
        return User.query.get(user_id)

    @staticmethod
    def get_all():
        """Get all users."""
        return User.query.all()

    @staticmethod
    def check_password(user, password):
        """Check whether the given password is correct."""
        return check_password_hash(user.pw_hash, password)
