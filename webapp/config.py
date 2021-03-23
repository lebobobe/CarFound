import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, '..', 'webapp.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
