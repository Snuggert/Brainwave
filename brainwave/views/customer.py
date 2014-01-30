"""admin.py - View for administration."""
from datetime import date, timedelta, datetime
from flask import render_template
from flask import Blueprint
from brainwave.controllers import AssociationController, \
    TransInController, ProductController, ProductCategoryController, \
    TransactionController
from brainwave.models import Stock, User
from brainwave.controllers.authentication import Authentication

customer_blueprint = Blueprint('customer', __name__, url_prefix='/customer')

@customer_blueprint.route('/credit', methods=['GET'])
@Authentication(User.ROLE_CUSTOMER)
def credit ():
    
    return render_template("customer/credit.htm", data={"credits":{}})
