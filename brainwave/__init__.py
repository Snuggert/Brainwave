from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Startup stuff
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Register blueprints
from brainwave.controllers.user import user_controller

app.register_blueprint(user_controller)
