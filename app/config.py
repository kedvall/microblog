import os
basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    DEBUG = False
    TETING = False
    CSRF_ENABLED = False
    SECRET_KEY = "MY-SUPER-SECRET-KEY"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'microblog_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(AppConfig):
    DEBUG = False


class DevelopmentConfig(AppConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(AppConfig):
    TESTING = True
