"""admin.py - View for administration."""
from flask import render_template
from flask import Blueprint
from brainwave.api import AssociationAPI, StockAPI, TransInAPI

admin_blueprint = Blueprint('admin', __name__,
                            url_prefix='/admin')


@admin_blueprint.route('/', methods=['GET'])
@admin_blueprint.route('/association', methods=['GET'])
def view_association(association_id=None):
    associations = AssociationAPI.get_all()
    return render_template('admin/association.htm',
                           data={'associations': associations})


@admin_blueprint.route('/stock', methods=['GET'])
def view_stock(user_id=None):
    stock = StockAPI.get_all()
    return render_template('admin/stock.htm', data={'stock': stock})


@admin_blueprint.route('/trans_in', methods=['GET'])
def view_trans_in(user_id=None):
    trans_in = TransInAPI.get_all()
    return render_template('admin/trans_in.htm', data={'trans_in': trans_in})
