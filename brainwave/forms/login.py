""" login_form.py - login form """

from flask.ext.wtf import Form
from brainwave.controllers.user import UserController
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me', default=False)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        user = UserController.get_by_name(
            username=self.username.data)

        if user is None:
            return False

        if not UserController.check_password(user, self.password.data):
            return False

        self.user = user
        return True
