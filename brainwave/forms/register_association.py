""" add_assoc_form.py - add association form """

from flask.ext.wtf import Form
from brainwave.forms.validation import Validation


class RegisterAssociationForm(Form):
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
