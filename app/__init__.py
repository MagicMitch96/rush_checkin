from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.basicauth import BasicAuth
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect

import os
import logging

# globals
LOG = logging.getLogger('werkzeug')
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# app configuration
app.config['SECRET_KEY'] = 'alphasig'

# use sqlite locally
if os.environ.get('DATABASE_URL') is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

# use postgres remote
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['BASIC_AUTH_USERNAME'] = 'alphasig'
app.config['BASIC_AUTH_PASSWORD'] = 'inphi1845'

# extensions
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
basic_auth = BasicAuth(app)
CsrfProtect(app)

from app import models
from app import views

db.create_all()
