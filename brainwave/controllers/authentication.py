from brainwave.views.login import *
from flask import session, redirect, url_for, request
from brainwave.controllers import UserController
from brainwave.models import User
from functools import wraps


class Authentication():
    def __init__(self, user_role):
        self.role = user_role

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if not session['user_id']:
                return redirect(url_for('login'))

            if session['user_role'] >= self.role:
                return func(*args, **kwargs)

            if request.json:
                return jsonify(error='Not allowed'), 403

            return render_template('403.htm')

        return wrapped_func
