from app import flask_app, db, cli
from app.models import User, Post


@flask_app.shell_context_processor
def make_shell_context():
    print("Added shell context")
    return {'db': db, 'User': User, 'Post': Post}


if __name__ == "__main__":
    flask_app.run()
