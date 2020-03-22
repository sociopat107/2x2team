from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import AnonymousUserMixin


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.login = 'Guest'

    def is_admin(self):
        return False
		
	def is_authenticated(self):
	    return False

app = Flask(__name__)
MAX_SEARCH_RESULTS = 10
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from app.models import User
from app import views

