# -*- coding: utf-8
from datetime import datetime


class InvalidInput(Exception):
    """
    Invalid input
    """

    def __init__(self, errors=None, message='Invalid input'):
        super(InvalidInput, self).__init__(message)
        self.when = datetime.now()
        self.errors = errors
        self.message = message


class Unauthorized(Exception):
    """
    Unauthorized
    """

    def __init__(self, errors=None, message='Unauthorized'):
        super(Unauthorized, self).__init__(message)
        self.when = datetime.now()
        self.errors = errors
        self.message = message
