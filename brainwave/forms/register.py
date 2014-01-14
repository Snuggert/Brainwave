""" register_form.py - register form """

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required
from brainwave.forms.validation import Validation
from brainwave.controllers import UserController


class RegisterForm(Form):
    username = TextField('Username',
                         validators=[Required(),
                                     Validation.validate_username()])
    email = TextField('Email',
                      validators=[Required(),
                                  Validation.validate_email()])
    password = PasswordField('Password',
                             validators=[Required(),
                                         Validation.validate_password()])
    password2 = PasswordField('Password again',
                              validators=[Required(),
                                          Validation.validate_password()])

    def validate(self):
        user = UserController.get_by_name(username=self.username.data)

        if user is not None:
            self.username.errors.append("Username already exists")
            return False

        user = UserController.get_by_email(email=self.email.data)

        if user is not None:
            self.email.errors.append("Email address already in use")
            return False

        if self.password.data is not self.password2.data:
            self.password.errors.append("Passwords do not match")
            return False

        return True
