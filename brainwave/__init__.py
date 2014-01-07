from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlite3 import dbapi2 as sqlite3

# Startup stuff
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Register blueprints
from brainwave.controllers.user import user_controller

app.register_blueprint(user_controller)
