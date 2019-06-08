# -*- coding: utf-8
import os


class BaseConfig(object):
    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secretkey')

    # Postgres database
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_USER = os.environ.get('DB_USER', 'sanic')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_DATABASE = os.environ.get('DB_NAME', 'development')

    # Bcrypt
    BCRYPT_LOG_ROUNDS = 12

    # Cookie settings
    SECURE_COOKIE = False
