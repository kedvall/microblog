import os
basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    # Flask config
    DEBUG = False
    TETING = False
    CSRF_ENABLED = False
    SECRET_KEY = "MY-SUPER-SECRET-KEY"
    # Database config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'microblog_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Email notification config
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USE_TLS = None
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    ADMINS = ['my_application@gmx.com']
    # Application config
    POSTS_PER_PAGE = 5
    LANGUAGES = ['en', 'es']


class ProductionConfig(AppConfig):
    DEBUG = False


class DevelopmentConfig(AppConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(AppConfig):
    TESTING = True
