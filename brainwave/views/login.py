""" login.py - Login view """
from flask import render_template, url_for, redirect, session, request
from brainwave import app
from brainwave.forms.login import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session['user_id'] = form.user.id

        # Do something good with it.
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.htm', form=form)
