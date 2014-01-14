# NOT DONE YET

""" register.py - User register form """
from brainwave.forms.register import RegisterForm

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # register User
