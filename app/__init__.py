import os
from flask import Flask

# Load config
flask_config = os.getenv('APP_CONFIG')
if flask_config is None:
    # print("- Warning: APP_SETTINGS not found")
    flask_config = 'DevelopmentConfig'

print(f"Name: {__name__}")
print(f"Config: {flask_config}")

# Create Flask instance
flask_app = Flask(__name__)
flask_app.config.from_object('app.config.' + flask_config)

from app import routes
