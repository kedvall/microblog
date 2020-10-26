from flask import render_template
from app import flask_app

@flask_app.route('/')
@flask_app.route('/index')
def index():
    user = {'username':'Kan'}
    posts = [
        {
            'author':{'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author':{'username': 'Susan'},
            'body': 'The avengers movie was so cool!'
        },
        {
            'author':{'username': 'Chad'},
            'body': 'Ah, okay'
        },
        {
            'author':{'username': 'Miguel'},
            'body': 'Flask is great'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
