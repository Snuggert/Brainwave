"""sale.py - View for POS interface (cash register)."""
from flask import render_template
from flask import Blueprint

pos_blueprint = Blueprint('pos', __name__,
                          url_prefix='/pos')


@pos_blueprint.route('/', methods=['GET'])
def pos_interface():
    return render_template('pos/view.htm')
