# -*- coding: utf-8
from datetime import datetime


class InvalidInput(Exception):
    """
    Invalid input
    """

    def __init__(self, message='Invalid input'):
        super(InvalidInput, self).__init__(message)
        self.when = datetime.now()


class Unauthorized(Exception):
    """
    Unauthorized
    """

    def __init__(self, message='Unauthorized'):
        super(Unauthorized, self).__init__(message)
        self.when = datetime.now()


class NotFound(Exception):
    """
    NotFound
    """

    def __init__(self, message='NotFound'):
        super(NotFound, self).__init__(message)
        self.when = datetime.now()
