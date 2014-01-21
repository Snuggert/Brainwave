""" login.py - Login view """
from flask import render_template, url_for, redirect, session
from brainwave import app
from brainwave.forms.login import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session['user_id'] = form.user.id
        session['user_role'] = form.user.role

        return redirect(url_for('admin.view_customers'))

    return render_template('login.htm', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['user_id'] = None
    session['user_role'] = None

    return redirect(url_for('login'))
