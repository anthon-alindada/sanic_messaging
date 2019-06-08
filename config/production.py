# -*- coding: utf-8
from .base import BaseConfig


class ProductionConfig(BaseConfig):
    # Cookie settings
    SECURE_COOKIE = True
