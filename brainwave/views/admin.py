"""user.py - View for user."""
from flask import flash, redirect, render_template, request, url_for, abort,\
    session
from flask import Blueprint
from brainwave.api import UserAPI, StockAPI, TransInAPI
from brainwave.utils import serialize_sqla

admin_blueprint = Blueprint('admin', __name__,
                            url_prefix='/admin')

@admin_blueprint.route('/', methods=['GET'])
@admin_blueprint.route('/user', methods=['GET'])
def view_user(user_id=None):
    users = UserAPI.get_all(); 
    return render_template('admin/users.htm', data={'users':users})

@admin_blueprint.route('/stock', methods=['GET'])
def view_stock(user_id=None):
    stock = StockAPI.get_all(); 
    return render_template('admin/stock.htm', data={'stock':stock})

@admin_blueprint.route('/trans_in', methods=['GET'])
def view_trans_in(user_id=None):
    trans_in = TransInAPI.get_all(); 
    return render_template('admin/trans_in.htm', data={'trans_in':trans_in})
