"""admin.py - View for administration."""
from flask import render_template
from flask import Blueprint
from flask.ext.login import login_required
from brainwave.controllers import AssociationController, StockController, \
    TransInController, ProductController, ProductCategoryController
from brainwave.utils import serialize_sqla
from brainwave.models import Stock

admin_blueprint = Blueprint('admin', __name__,
                            url_prefix='/admin')


@admin_blueprint.route('/', methods=['GET'])
@admin_blueprint.route('/association', methods=['GET'])
@login_required
def view_association(association_id=None):
    associations = AssociationController.get_all()
    return render_template('admin/association.htm',
                           data={'associations': associations})


@admin_blueprint.route('/stock', methods=['GET'])
@admin_blueprint.route('/stock/<string:query>', methods=['GET'])
@login_required
def view_stock(user_id=None, query=""):
    if query != "":
        stock = StockController.get_all_from(query)
    else:
        stock = StockController.get_all()

    return render_template('admin/stock.htm', data={'stock': stock})


@admin_blueprint.route('/stock/new', methods=['GET'])
@login_required
def new_stock(user_id=None):
    associations = AssociationController.get_all()
    return render_template('admin/new_stock.htm',
                           data={'stock': {},
                                 'associations': associations})


@admin_blueprint.route('/trans_in', methods=['GET'])
@login_required
def view_trans_in(user_id=None):
    trans_in = TransInController.get_all()
    return render_template('admin/trans_in.htm', data={'trans_in': trans_in})


@admin_blueprint.route('/product', methods=['GET'])
@login_required
def view_product(user_id=None):
    products = ProductController.get_all()
    return render_template('admin/product.htm', data={'products': products})


@admin_blueprint.route('/post', methods=['GET'])
def view_post_tmp(user_id=None):
    return render_template('admin/post.html', data={'bla': 'bla2'})


@admin_blueprint.route('/product/new', methods=['GET'])
@login_required
def new_product(user_id=None):
    stocks = Stock.query.all()
    product_categories = ProductCategoryController.get_all()
    associations = AssociationController.get_all()
    return render_template('admin/new_product.htm',
                           data={'stocks': stocks,
                                 'product_categories': product_categories,
                                 'product': {}, 'associations': associations})
