import os
basedir = os.path.abspath(os.path.dirname(__file__))


CSRF_ENABLED = True
SECRET_KEY = 'iupahngooRohj3gaeghienaebaewaikeegeeng4Ae'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'project.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
