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
app.config.from_pyfile('config.py')

# use sqlite locally
if os.environ.get('DATABASE_URL') is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

# use postgres remote
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

# extensions
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
basic_auth = BasicAuth(app)
CsrfProtect(app)

# heroku logging
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('rushcheckin startup')

from app import models
from app import views

db.create_all()
