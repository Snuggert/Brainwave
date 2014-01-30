"""customer.py - Display customers credits"""
from datetime import date, timedelta, datetime
from flask import render_template
from flask import Blueprint
from flask import session
from flask import jsonify
from brainwave.controllers import CreditController, UserController, \
                                  AssociationController
from brainwave.models import Credit, Customer, Association, User
from brainwave.controllers.authentication import Authentication

customer_blueprint = Blueprint('customer', __name__, url_prefix='/customer')

@customer_blueprint.route('/credit', methods=['GET'])
@Authentication(User.ROLE_CUSTOMER)
def credit ():
    
    customer = Customer.query.filter_by(user_id=session["user_id"]).first()
    credits =  Credit.query.filter_by(customer_id=customer.id).all()
    return render_template("customer/credit.htm", data={"credits":credits})