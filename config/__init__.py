# -*- coding: utf-8
from .development import DevelopmentConfig
from .production import ProductionConfig
from .test import TestConfig


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'default': DevelopmentConfig,
}
