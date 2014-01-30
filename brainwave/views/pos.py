"""sale.py - View for POS interface (cash register)."""
from flask import render_template
from flask import Blueprint
from brainwave.controllers.authentication import Authentication
from brainwave.models import User

pos_blueprint = Blueprint('pos', __name__,
                          url_prefix='/pos')


@pos_blueprint.route('/', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def pos_interface():
    return render_template('pos/view.htm')
