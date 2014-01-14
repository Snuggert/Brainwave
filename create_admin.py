from brainwave.controllers.user import User
from werkzeug.security import generate_password_hash
from brainwave import db

user = User('admin', generate_password_hash('1234'), 'bladie@bla.nl', 8)

db.session.add(user)
db.session.commit()
