from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Startup stuff
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Register blueprints
from brainwave.controllers import *
from brainwave.views.admin import admin_blueprint

app.register_blueprint(association_controller)
app.register_blueprint(stock_controller)
app.register_blueprint(trans_in_controller)
app.register_blueprint(product_category_controller)
app.register_blueprint(product_controller)
app.register_blueprint(admin_blueprint)

# Add methods and modules to jinja environment
from brainwave.utils import serialize_sqla
import json
app.jinja_env.globals.update(json=json)
app.jinja_env.globals.update(serialize_sqla=serialize_sqla)
