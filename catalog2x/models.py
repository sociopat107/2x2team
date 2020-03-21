from . import db,app
import datetime

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    boti = db.relationship('Bot', backref = 'user', lazy = 'dynamic')


    def __init__(self, username='', password='', role=0):
        self.login = username
        self.role = role
        self.password = password

    def is_authenticated(self):
        return True

    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.login)
