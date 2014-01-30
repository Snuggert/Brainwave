""" login.py - Login view """
from flask import render_template, url_for, redirect, session
from brainwave import app
from brainwave.forms.login import LoginForm
from brainwave.controllers import UserController
from brainwave.models.user import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('admin.view_customers'))

    form = LoginForm()

    if form.validate_on_submit():
        session['user_id'] = form.user.id
        session['user_role'] = form.user.role

        if (form.user.role == User.ROLE_ADMIN):
            return redirect(url_for('admin.view_customers'))
        if (form.user.role == User.ROLE_ASSOCIATION):
            user = UserController.get(session['user_id'])
            session['association_id'] = user.association[0].id

            return redirect(url_for('admin.view_customers'))
        if (form.user.role == User.ROLE_CUSTOMER):
            return redirect(url_for('customer.credit'))

    return render_template('login.htm', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    UserController.logout()

    return redirect(url_for('login'))
