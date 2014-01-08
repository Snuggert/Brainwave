import os
import sys

from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlite3 import dbapi2 as sqlite3

# Startup stuff
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Register blueprints
from .brainwave.controllers.user import user_controller
from .brainwave.views.admin import admin_blueprint

app.register_blueprint(user_controller)
app.register_blueprint(admin_blueprint)

# Add methods and modules to jinja environment
from .brainwave.utils import serialize_sqla
app.jinja_env.globals.update(json=json)
app.jinja_env.globals.update(serialize_sqla=serialize_sqla)