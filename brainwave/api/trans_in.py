"""trans_in.py - Controller for transaction-in."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import TransInController
from brainwave.utils import serialize_sqla

trans_in_api = Blueprint('trans_in_api', __name__,
                         url_prefix='/api/trans_in')


@trans_in_api.route('', methods=['POST'])
def create():
    """Create new trans_in item."""
    trans_in_dict = request.json

    trans_in = TransInController.create(trans_in_dict)

    return jsonify(id=trans_in.id)


@trans_in_api.route('/<int:trans_in_id>', methods=['DELETE'])
def delete(trans_in_id):
    """Delete trans_in item."""
    trans_in = TransInController.get(trans_in_id)

    if not trans_in:
        return jsonify(error='Transaction-in item not found'), 500

    TransInController.delete(trans_in)

    return jsonify()


@trans_in_api.route('/<int:trans_in_id>', methods=['GET'])
def get(trans_in_id):
    """Get trans_in item."""
    trans_in = TransInController.get(trans_in_id)

    if not trans_in:
        return jsonify(error='Transaction-in item not found'), 500

    return jsonify(trans_in=serialize_sqla(trans_in))
