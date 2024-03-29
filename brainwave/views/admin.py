"""admin.py - View for administration."""
from datetime import date, timedelta, datetime
from flask import render_template, session, Blueprint
from brainwave.controllers import AssociationController, \
    ProductController, ProductCategoryController, \
    TransactionController, TransactionPieceController, StockController
from brainwave.models import Stock, User, Association
from brainwave.controllers.authentication import Authentication

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route('', methods=['GET'])
@admin_blueprint.route('/customer', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def view_customers():
    return render_template('admin/customer.htm')


@admin_blueprint.route('/association', methods=['GET'])
@Authentication(User.ROLE_ADMIN)
def view_associations():
    return render_template('admin/association.htm')


@admin_blueprint.route('/product_category', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def view_product_category():
    return render_template('admin/product_category.htm')


@admin_blueprint.route('/stock', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def view_stock(user_id=None, query=""):
    stock = StockController.get_all()

    return render_template('admin/stock.htm', data={'stock': stock})


@admin_blueprint.route('/stock/new', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def new_stock(user_id=None):
    associations = AssociationController.get_all()
    return render_template('admin/new_stock.htm',
                           data={'stock': {},
                                 'associations': associations})


@admin_blueprint.route('/trans_in', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def view_trans_in(user_id=None):
    stocks = StockController.get_all()
    associations = AssociationController.get_all()
    return render_template('admin/trans_in.htm',
                           data={'stocks': stocks,
                                 'associations': associations})


@admin_blueprint.route('/product', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def view_product(user_id=None):
    products = ProductController.get_all()
    return render_template('admin/product.htm', data={'products': products})


@admin_blueprint.route('/cashier', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def view_cashier():
    assoc = Association.query.filter_by(id=session['association_id']).first()
    cash_amount = AssociationController.get_cash_counter(assoc)

    return render_template('admin/cashier.htm',
                           data={'cash_amount': cash_amount})


@admin_blueprint.route('/product/new', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def new_product(user_id=None):
    stocks = Stock.query.all()
    product_categories = ProductCategoryController.get_all()
    associations = AssociationController.get_all()

    return render_template('admin/new_product.htm',
                           data={'stocks': stocks,
                                 'product_categories': product_categories,
                                 'product': {}, 'associations': associations})


@admin_blueprint.route('/analysis', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
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

    if session['user_role'] >= 8:
        for association in AssociationController.get_all():
            graphdata[association.name] = []
    elif session['user_role'] >= 4:
        assocation = AssociationController.get(session['association_id'])
        graphdata[assocation.name] = []

    for transaction in week_transactions:
        epoch_seconds = (transaction.created -
                         datetime(1970, 1, 1)).total_seconds() * 1000
        sale_price = 0
        for piece in transaction.pieces:
            sale_price += piece.price
        graphdata[transaction.association.name].append([epoch_seconds,
                                                        sale_price,
                                                        transaction.id])

    print "Week Number", week_number
    return render_template('admin/analysis.htm',
                           data={'graphdata': graphdata,
                                 'week_number': week_number,
                                 'epoch_week_start': epoch_week_start,
                                 'epoch_week_end': epoch_week_end})


@admin_blueprint.route('/sales', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def sales(user_id=None):

    transactions = TransactionPieceController.get_all_merged()

    return render_template('admin/sales.htm',
                           data={'transactions': transactions})


def first_monday(year, week):
    d = date(year, 1, 4)  # The Jan 4th must be in week 1  according to ISO
    return d + timedelta(weeks=(week - 1), days =- d.weekday())
