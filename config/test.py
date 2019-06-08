# -*- coding: utf-8
from .base import BaseConfig


class TestConfig(BaseConfig):
    # Test postgres database
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_USER = 'sanic'
    DB_PASSWORD = 'password'
    DB_DATABASE = 'test'
