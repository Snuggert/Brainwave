""" login_form.py - login form """

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember = BooleanField('remember', default=False)
