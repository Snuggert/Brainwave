"""user.py - View for user."""
from flask import flash, redirect, render_template, request, url_for, abort,\
    session
from flask import Blueprint
from brainwave.api.user import UserAPI
from brainwave.utils import serialize_sqla

admin_blueprint = Blueprint('admin', __name__,
                            url_prefix='/admin')

@admin_blueprint.route('/', methods=['GET'])
@admin_blueprint.route('/user', methods=['GET'])
def view_user(user_id=None):
    users = UserAPI.get_all();
    return render_template('admin/users.htm', users=users)
