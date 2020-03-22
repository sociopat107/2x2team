from app import db,app
import datetime
import flask.ext.whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):    
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120)) 
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __init__(self, username='', email='', password='', role=0):
        self.login = username
        self.email = email
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

class Category(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    photo = db.Column(db.String(128), index = True, unique = True)
    tovari = db.relationship('Tovar', backref = 'category', lazy = 'dynamic')

    def __init__(self, title='', photo=''):
        self.name = title
        self.photo = photo

    def __repr__(self):
        return '<Category %r>' % self.id


class Tovar(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    photo = db.Column(db.String(128), index = True, unique = True)
    price = db.Column(db.Integer) 
    date = db.Column(db.DateTime)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))


    def __init__(self, title='', photo='', price='', pub_date=''):
        self.name = title
        self.photo = photo
        self.price = price
        pub_date = datetime.datetime.utcnow()
        self.date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.name


whooshalchemy.whoosh_index(app, Tovar)
