"""user.py - Controller for user."""
from flask import Blueprint, jsonify, request
from brainwave.api.user import UserAPI
from brainwave.utils import serialize_sqla

user_controller = Blueprint('user_controller', __name__,
                            url_prefix='/api/user')


@user_controller.route('/', methods=['POST'])
def create():
    """Create a new user."""
    user_dict = request.json

    try:
        user = UserAPI.create(user_dict)
    except UserAPI.NoPassword as e:
        return jsonify(error=e.error), 500

    return jsonify(id=user.id, pw_hash=user.pw_hash)


@user_controller.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    """Update a user."""
    user_dict = request.json

    user = UserAPI.update(user_dict)

    return jsonify(pw_hash=user.pw_hash)


@user_controller.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    """Delete a user."""
    user = UserAPI.get(user_id)

    if not user:
        return jsonify(error='User not found'), 500

    return jsonify()


@user_controller.route('/<int:user_id>', methods=['GET'])
def get(user_id):
    """Get a user."""
    user = UserAPI.get(user_id)

    if not user:
        return jsonify(error='User not found'), 500

    return jsonify(user=serialize_sqla(user))
