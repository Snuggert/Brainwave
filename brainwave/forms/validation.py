""" validation.py - validation class """

import re


class Validation():
    """ Class that contains validation functions """

    def validate_username(form, field):
        """ Validates username. Must start with a letter, follow by letters,
        numbers, - or _. Minimum length is 5 characters.
        """
        return re.match(r'[A-Za-z]+[A-Za-z0-9]{4,}', field.data)

    def validate_password(form, field):
        """ Validates password. Minimum length is 8 characters, can contain
        letters, numbers, @, #, $, %, ^ & + and =.
        """
        return re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', field.data)

    def validate_email(form, field):
        pass
