import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from redis import Redis
import rq
from elasticsearch import Elasticsearch
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import DevelopmentConfig


db = SQLAlchemy()           # Database setup
migrate = Migrate()
login = LoginManager()      # Login setup
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()               # Mail setup
bootstrap = Bootstrap()     # Bootstrap setup
moment = Moment()           # Timezone management
babel = Babel()             # Localization


def create_app(config_class=DevelopmentConfig):
    # Load config
    flask_config = os.environ.get('APP_CONFIG') or 'DevelopmentConfig'

    # print(f"Name: {__name__}")
    # print(f"Config: {flask_config}")

    # Create Flask instance
    flask_app = Flask(__name__)
    flask_app.config.from_object('config.' + flask_config)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    login.init_app(flask_app)
    mail.init_app(flask_app)
    bootstrap.init_app(flask_app)
    moment.init_app(flask_app)
    babel.init_app(flask_app)

    flask_app.elasticsearch = Elasticsearch(
        [flask_app.config['ELASTICSEARCH_URL']]) if flask_app.config['ELASTICSEARCH_URL'] else None

    flask_app.redis = Redis.from_url(flask_app.config['REDIS_URL'])
    flask_app.task_queue = rq.Queue('microblog-tasks', connection=flask_app.redis)

    from app.errors import bp as errors_bp
    flask_app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    flask_app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    flask_app.register_blueprint(api_bp, url_prefix='/api')

    # Logging setup
    if not flask_app.debug and not flask_app.testing:
        if flask_app.config['MAIL_SERVER']:
            auth = None
            if flask_app.config['MAIL_USERNAME'] or flask_app.config['MAIL_PASSWORD']:
                auth = (flask_app.config['MAIL_USERNAME'], flask_app.config['MAIL_PASSWORD'])
            secure = None
            if flask_app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(flask_app.config['MAIL_SERVER'], flask_app.config['MAIL_PORT']),
                fromaddr='no-reply@' + flask_app.config['MAIL_SERVER'],
                toaddrs=flask_app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            flask_app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
        file_handler.setLevel(logging.INFO)
        flask_app.logger.addHandler(file_handler)

        flask_app.logger.setLevel(logging.INFO)
        flask_app.logger.info('Microblog startup')

    return flask_app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
