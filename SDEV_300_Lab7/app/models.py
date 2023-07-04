'''User class'''
from flask_login import UserMixin
from app import login_manager
from passlib.hash import sha256_crypt

class User(UserMixin):
    '''User class with set password function'''
    def __init__(self, username):
        '''Sets username'''
        self.username = username
        # load_user needs an id attribute so id = username
        self.id = username

    def set_password(self, password):
        '''Sets encrypted password'''
        self.password = sha256_crypt.hash(password)

@login_manager.user_loader
def load_user(user_id):
    '''Needed for flask_login. Loads user object based on username'''
    return User(user_id)
