# import os
# basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    DEBUG = False
    TETING = False
    CSRF_ENABLED = False
    SECRET_KEY = "MY-SUPER-SECRET-KEY"


class ProductionConfig(AppConfig):
    DEBUG = False


class DevelopmentConfig(AppConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(AppConfig):
    TESTING = True
