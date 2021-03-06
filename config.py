import os

basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig(object):
    # Flask config
    DEBUG = False
    TETING = False
    CSRF_ENABLED = False
    SECRET_KEY = "MY-SUPER-SECRET-KEY"
    # Database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'microblog_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Email notification config
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 8025
    MAIL_USE_TLS = None
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    ADMINS = ['my_application@gmx.com']
    # Application config
    POSTS_PER_PAGE = 5
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = '00c0a5eb46d64346a935576109145504'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'


class ProductionConfig(AppConfig):
    DEBUG = False


class DevelopmentConfig(AppConfig):
    DEVELOPMENT = True
    DEBUG = True
