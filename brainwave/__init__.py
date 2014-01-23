from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required
from sqlite3 import dbapi2 as sqlite3

# Startup stuff
app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

# Register blueprints
from brainwave.api import *
from brainwave.views.admin import admin_blueprint
from brainwave.views.sale import sale_blueprint
from brainwave.views.pos import pos_blueprint
from brainwave.views.login import *

app.register_blueprint(user_api)
app.register_blueprint(association_api)
app.register_blueprint(stock_api)
app.register_blueprint(trans_in_api)
app.register_blueprint(product_category_api)
app.register_blueprint(product_api)
app.register_blueprint(customer_api)
app.register_blueprint(credit_api)
app.register_blueprint(admin_blueprint)
app.register_blueprint(sale_blueprint)
app.register_blueprint(pos_blueprint)
app.register_blueprint(transaction_api)


@app.errorhandler(404)
@login_required
def page_not_found(e):
    return render_template('404.htm'), 404

# Add methods and modules to jinja environment
from brainwave.utils import serialize_sqla
import json
app.jinja_env.globals.update(json=json)
app.jinja_env.globals.update(serialize_sqla=serialize_sqla)
