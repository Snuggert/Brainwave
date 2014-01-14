"""transaction.py - Transaction for user."""
from flask import Blueprint, jsonify, request
from brainwave.controllers.transaction import TransactionController
from brainwave.utils import serialize_sqla

transaction_api = Blueprint('transaction_api', __name__,
                            url_prefix='/api/transaction')


@transaction_api.route('/new', methods=['POST'])
def create():
    """Create a new transaction."""
    dict = request.json

    print dict

    return jsonify(random='Yeah!'), 500


# @user_api.route('/<int:user_id>', methods=['PUT'])
# def update(user_id):
#     """Update a user."""
#     user_dict = request.json

#     user = UserController.update(user_dict)

#     return jsonify(pw_hash=user.pw_hash)


# @user_api.route('/<int:user_id>', methods=['DELETE'])
# def delete(user_id):
#     """Delete a user."""
#     user = UserController.get(user_id)

#     if not user:
#         return jsonify(error='User not found'), 500

#     UserController.delete(user)

#     return jsonify()


# @user_api.route('/<int:user_id>', methods=['GET'])
# def get(user_id):
#     """Get a user."""
#     user = UserController.get(user_id)

#     if not user:
#         return jsonify(error='User not found'), 500

#     return jsonify(user=serialize_sqla(user))


# # Work in progress
# @user_api.route('/login', methods=['GET', 'POST'])
# def login():
#     pass
