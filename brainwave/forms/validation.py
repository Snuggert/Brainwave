""" validation.py - validation class """

import re


class Validation():
    """ Class that contains validation functions """

    def validate_username(username):
        """ Validates username. Must start with a letter, follow by letters,
        numbers, - or _. Minimum length is 5 characters.
        """
        return re.match(r'[A-Za-z]+[A-Za-z0-9_-]{4,}', username)

    def validate_password(password):
        """ Validates password. Minimum length is 8 characters, can contain
        letters, numbers, @, #, $, %, ^ & + and =.
        """
        return re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password)

    def validate_email(email):
        # Yet to be implemented
        return False
