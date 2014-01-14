from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from sqlite3 import dbapi2 as sqlite3

# Startup stuff
app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

# Register blueprints
from brainwave.controllers import *
from brainwave.api import *
from brainwave.views.admin import admin_blueprint
from brainwave.views.login import *


app.register_blueprint(user_api)
app.register_blueprint(association_api)
app.register_blueprint(stock_controller)
app.register_blueprint(trans_in_controller)
app.register_blueprint(product_category_controller)
app.register_blueprint(product_controller)
app.register_blueprint(customer_controller)
app.register_blueprint(admin_blueprint)

# Add methods and modules to jinja environment
from brainwave.utils import serialize_sqla
import json
app.jinja_env.globals.update(json=json)
app.jinja_env.globals.update(serialize_sqla=serialize_sqla)
