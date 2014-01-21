from brainwave.views.login import *
from flask import session, redirect, url_for
from brainwave.controllers import UserController


class Authentication():
    def __init__(self, admin=False, association=False, barteam=False,
                 customer=False):
        self.admin = admin
        self.association = association
        self.barteam = barteam
        self.customer = customer

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):

            if not session['user_id']:
                return redirect(url_for('login'))

            user = UserController.get(session['user_id'])

            if self.admin and UserController.is_admin(user):
                return func(*args, **kwargs)

            if self.association \
                    and kwargs['ass_id'] == UserController.is_association(user):

                return func(*args, **kwargs)

            if self.customer \
                    and kwargs['cust_id'] == UserController.is_customer(user):
                return func(*args, **kwargs)

            return render_template('403.htm')

        return wrapped_func
