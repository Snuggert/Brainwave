"""user.py - Controller for user."""
from werkzeug.security import generate_password_hash, check_password_hash
from brainwave.models.user import User
from brainwave import db, login_manager
from flask.ext.login import login_user, logout_user
from flask import session


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class UserController:
    """The API for user manipulation."""
    class NoPassword(Exception):
        """Exception for when a password is missing."""
        def __init__(self):
            """Initialize with a standard message."""
            self.error = 'No password given'

    class UsernameTaken(Exception):
        """Exception when username already taken """
        def __init__(self):
            self.error = 'Username already in taken'

    class EmailInUse(Exception):
        """Exception when email address is already in use """
        def __init__(self):
            self.error = 'Email address already in use'

    class NoPasswordMatch(Exception):
        """Exception when passwords don't match """
        def __init__(self):
            self.error = 'Passwords don\'t match'

    class PasswordIncorrect(Exception):
        """Exception when password is incorrect """
        def __init__(self):
            self.error = 'Password incorrect'

    @staticmethod
    def create(user_dict):
        """Create a new user."""
        password = user_dict.pop('password', None)
        if not password:
            raise UserController.NoPassword()

        user = UserController.get_by_name(user_dict['login_name'])
        if user:
            raise UserController.UsernameTaken()

        user = UserController.get_by_email(user_dict['email'])
        if user:
            raise UserController.EmailInUse()

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
    def get_by_name(username):
        user = User.query.filter_by(login_name=username).first()

        return user

    @staticmethod
    def get_by_email(email):
        user = User.query.filter_by(email=email).first()

        return user

    @staticmethod
    def get_all():
        """Get all users."""
        return User.query.all()

    @staticmethod
    def check_password(user, password):
        """Check whether the given password is correct."""
        return check_password_hash(user.pw_hash, password)

    @staticmethod
    def login(username, password, remember):
        user = UserController.get_by_name(username)

        if not user:
            return False

        if UserController.check_password(user, password):
            if login_user(user, remember):
                session.user_id = user.id
                session.user_role = user.role

                return user
        else:
            raise UserController.PasswordIncorrect()

        return False

    @staticmethod
    def logout():
        logout_user()

        return

    @staticmethod
    def is_admin(user):
        if user.role == User.ROLE_ADMIN:
            return True
        else:
            return None

    @staticmethod
    def get_association(user):
        if user.role == User.ROLE_ASSOCIATION:
            return user.association
        else:
            return None

    @staticmethod
    def get_customer(user):
        if user.role == User.ROLE_CUSTOMER:
            return user.customer
        else:
            return None
