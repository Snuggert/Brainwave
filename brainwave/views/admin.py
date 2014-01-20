"""admin.py - View for administration."""
from datetime import date, timedelta, datetime
from flask import render_template
from flask import Blueprint
from brainwave.controllers import AssociationController, StockController, \
    TransInController, ProductController, ProductCategoryController, \
    TransactionController, Authentication
from brainwave.models import Stock

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route('/<int:ass_id>/customer', methods=['GET'])
@Authentication(admin=True, association=True)
def view_customers(ass_id):
    return render_template('admin/customer.htm')


@admin_blueprint.route('/', methods=['GET'])
@admin_blueprint.route('/association', methods=['GET'])
def view_associations():
    return render_template('admin/association.htm')


@admin_blueprint.route('/stock', methods=['GET'])
@admin_blueprint.route('/stock/<string:query>', methods=['GET'])
def view_stock(user_id=None, query=""):
    if query != "":
        stock = StockController.get_all_from(query)
    else:
        stock = StockController.get_all()

    return render_template('admin/stock.htm', data={'stock': stock})


@admin_blueprint.route('/stock/new', methods=['GET'])
def new_stock(user_id=None):
    associations = AssociationController.get_all()
    return render_template('admin/new_stock.htm',
                           data={'stock': {},
                                 'associations': associations})


@admin_blueprint.route('/trans_in', methods=['GET'])
def view_trans_in(user_id=None):
    trans_in = TransInController.get_all()
    return render_template('admin/trans_in.htm', data={'trans_in': trans_in})


@admin_blueprint.route('/product', methods=['GET'])
def view_product(user_id=None):
    products = ProductController.get_all()
    return render_template('admin/product.htm', data={'products': products})


@admin_blueprint.route('/post', methods=['GET'])
def view_post_tmp(user_id=None):
    return render_template('admin/post.html', data={'bla': 'bla2'})


@admin_blueprint.route('/product/new', methods=['GET'])
def new_product(user_id=None):
    stocks = Stock.query.all()
    product_categories = ProductCategoryController.get_all()
    associations = AssociationController.get_all()
    return render_template('admin/new_product.htm',
                           data={'stocks': stocks,
                                 'product_categories': product_categories,
                                 'product': {}, 'associations': associations})


@admin_blueprint.route('/analysis', methods=['GET'])
@Authentication(admin=True, association=True)
def view_analysis(user_id=None):
    week_year, week_number, week_day = date.today().isocalendar()
    week_monday = first_monday(week_year, week_number)
    week_transactions = TransactionController.\
        get_between(week_monday, week_monday + timedelta(7))

    datetime_monday = datetime.combine(week_monday, datetime.min.time())
    epoch_week_start = (datetime_monday -
                        datetime(1970, 1, 1)).total_seconds() * 1000
    epoch_week_end = ((datetime_monday + timedelta(7)) -
                      datetime(1970, 1, 1)).total_seconds() * 1000
    graphdata = {}
    for association in AssociationController.get_all():
        graphdata[association.name] = []

    for transaction in week_transactions:
        epoch_seconds = (transaction.created -
                         datetime(1970, 1, 1)).total_seconds() * 1000
        sale_price = 0
        for piece in transaction.pieces:
            sale_price += piece.price
        graphdata[transaction.association.name].append([epoch_seconds,
                                                        sale_price])

    return render_template('admin/analysis.htm',
                           data={'graphdata': graphdata,
                                 'week_number': week_number,
                                 'epoch_week_start': epoch_week_start,
                                 'epoch_week_end': epoch_week_end})


def first_monday(year, week):
    d = date(year, 1, 4)  # The Jan 4th must be in week 1  according to ISO
    return d + timedelta(weeks=(week - 1), days =- d.weekday())
