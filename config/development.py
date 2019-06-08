# -*- coding: utf-8
from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    # Cookie settings
    SECURE_COOKIE = False
