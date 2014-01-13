"""sale.py - View for sale interface (cash register)."""
from flask import render_template
from flask import Blueprint
from brainwave.api import AssociationAPI, StockAPI, TransInAPI, ProductAPI, \
    ProductCategoryAPI
from brainwave.utils import serialize_sqla
from brainwave.models import Stock

sale_blueprint = Blueprint('sale', __name__,
                            url_prefix='/sale')


@sale_blueprint.route('/', methods=['GET'])
def sale_interface():
    return render_template('sale/view.htm')