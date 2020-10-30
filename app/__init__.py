import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

# Load config
flask_config = os.getenv('APP_CONFIG')
if flask_config is None:
    # print("- Warning: APP_SETTINGS not found")
    flask_config = 'DevelopmentConfig'
    # flask_config = 'ProductionConfig'

print(f"Name: {__name__}")
print(f"Config: {flask_config}")

# Create Flask instance
flask_app = Flask(__name__)
flask_app.config.from_object('app.config.' + flask_config)

# Database setup
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

# Login setup
login = LoginManager(flask_app)
login.login_view = 'login'

# Mail setup
mail = Mail(flask_app)

# Logging setup
if not flask_app.debug:
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
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
    file_handler.setLevel(logging.INFO)
    flask_app.logger.addHandler(file_handler)

    flask_app.logger.setLevel(logging.INFO)
    flask_app.logger.info('Microblog startup')

from app import routes, models, errors
