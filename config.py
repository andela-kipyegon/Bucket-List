import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ Base class for config class"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    URL_PREFIX = '/api'
    SECRET_KEY = os.getenv('SECRET_KEY', 'place-the-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',\
                                'postgresql://localhost/bucket_list')

class ProductionConfig(Config):
    """ Config class for prodxn"""
    DEBUG = False


class StagingConfig(Config):
    """ Config class Staging  """

    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """ Config for development"""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """ Config for testing"""

    TESTING = True
