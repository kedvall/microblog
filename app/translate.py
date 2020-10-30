import json
import requests
from flask_babel import _
from app import flask_app


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in flask_app.config or not flask_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: The translation service is not configured')
    auth = {'Ocp-Apim-Subscription-Key': flask_app.config['MS_TRANSLATOR_KEY']}
    request = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
        f'/Translate?text={text}&from={source_language}&to={dest_language}', headers=auth)
    if request.status_code != 200:
        return _('Error: The translation service failed')
    return json.loads(request.content.decode('utf-8-sig'))
