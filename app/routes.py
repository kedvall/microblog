from flask import render_template, flash, redirect, url_for
from app import flask_app
from app.forms import LoginForm

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

@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
