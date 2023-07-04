'''Creates instance of Flask app object
Some credits to Miguel Grinberg's flask tutorial:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
https://github.com/miguelgrinberg/microblog/
mostly the use of UserMixin and separation of concerns'''

from flask import Flask
from flask_login import LoginManager
import secrets

# needed for session/privacy control
login_manager = LoginManager()

def create_app():
    '''Creates instance of Flask application'''
    app = Flask(__name__)
    login_manager.init_app(app)
    # need a secret key for CSRF protection
    SECRET_KEY = secrets.token_hex()
    app.config["SECRET_KEY"] = SECRET_KEY
    return app
