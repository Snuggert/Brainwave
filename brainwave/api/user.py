"""user.py - API for user."""
from flask import Blueprint, jsonify, request
from brainwave.controllers.user import UserController
from brainwave.utils import serialize_sqla

user_api = Blueprint('user_api', __name__, url_prefix='/api/user')


@user_api.route('', methods=['POST'])
def create():
    """Create a new user."""
    user_dict = request.json

    try:
        user = UserController.create(user_dict)
    except UserController as e:
        return jsonify(error=e.error), 500

    return jsonify(id=user.id, pw_hash=user.pw_hash)


@user_api.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    """Update a user."""
    user_dict = request.json

    user = UserController.update(user_dict)

    return jsonify(pw_hash=user.pw_hash)


@user_api.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    """Delete a user."""
    user = UserController.get(user_id)

    if not user:
        return jsonify(error='User not found'), 500

    UserController.delete(user)

    return jsonify()


@user_api.route('/<int:user_id>', methods=['GET'])
def get(user_id):
    """Get a user."""
    user = UserController.get(user_id)

    if not user:
        return jsonify(error='User not found'), 500

    return jsonify(user=serialize_sqla(user))


@user_api.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    remember = request.form['remember']

    user = UserController.login(username, password, remember)

    if not user:
        return jsonify(id=user.id)
    else:
        return jsonify(error='Username or password incorrect'), 500


@user_api.route('/logout', methods=['GET', 'POST'])
def logout():
    UserController.logout()

    return jsonify()
