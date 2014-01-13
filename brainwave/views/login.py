""" login.py - Login view """
from flask import render_template
from brainwave import app
from brainwave.forms.loginform import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template('login.htm', form=form)
