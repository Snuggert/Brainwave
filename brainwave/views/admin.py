"""admin.py - View for administration."""
from flask import render_template
from flask import Blueprint
from brainwave.api import AssociationAPI, StockAPI, TransInAPI, ProductAPI, \
    ProductCategoryAPI
from brainwave.utils import serialize_sqla
from brainwave.models import Stock

admin_blueprint = Blueprint('admin', __name__,
                            url_prefix='/admin')


@admin_blueprint.route('/', methods=['GET'])
@admin_blueprint.route('/association', methods=['GET'])
def view_association(association_id=None):
    associations = AssociationAPI.get_all()
    return render_template('admin/association.htm',
                           data={'associations': associations})


@admin_blueprint.route('/stock', methods=['GET'])
@admin_blueprint.route('/stock/<string:query>', methods=['GET'])
def view_stock(user_id=None, query=""):
    stock = StockAPI.get_all_from(query)
    return render_template('admin/stock.htm', data={'stock':stock})


@admin_blueprint.route('/stock/new', methods=['GET'])
def new_stock(user_id=None):
    return render_template('admin/new_stock.htm', data={})


@admin_blueprint.route('/trans_in', methods=['GET'])
def view_trans_in(user_id=None):
    trans_in = TransInAPI.get_all()
    return render_template('admin/trans_in.htm', data={'trans_in': trans_in})


@admin_blueprint.route('/product', methods=['GET'])
def view_product(user_id=None):
    products = ProductAPI.get_all()
    return render_template('admin/product.htm', data={'products': products})


@admin_blueprint.route('/product/new', methods=['GET'])
def new_product(user_id=None):
    stocks = Stock.query.all()
    product_categories = ProductCategoryAPI.get_all()
    return render_template('admin/new_product.htm', data={'stocks': stocks,
                           'product_categories': product_categories})