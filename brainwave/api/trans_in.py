"""trans_in.py - Controller for transaction-in."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import TransInController
from brainwave.utils import serialize_sqla
from brainwave.controllers.authentication import Authentication
from brainwave.models import User

trans_in_api = Blueprint('trans_in_api', __name__,
                         url_prefix='/api/trans_in')


@trans_in_api.route('', methods=['POST'])
@Authentication(User.ROLE_ASSOCIATION)
def create():
    """Create new trans_in item."""
    trans_in_dict = request.json

    trans_in = TransInController.create(trans_in_dict)

    return jsonify(id=trans_in.id), 200


@trans_in_api.route('/delete/<int:trans_in_id>', methods=['DELETE'])
@Authentication(User.ROLE_ASSOCIATION)
def delete(trans_in_id):
    """Delete trans_in item."""
    trans_in = TransInController.get(trans_in_id)

    if not trans_in:
        return jsonify(error='Transaction-in item not found'), 500

    TransInController.delete(trans_in)

    return jsonify()


@trans_in_api.route('/<int:trans_in_id>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get(trans_in_id):
    """Get trans_in item."""
    trans_in = TransInController.get(trans_in_id)

    if not trans_in:
        return jsonify(error='Transaction-in item not found'), 500

    return jsonify(trans_in=serialize_sqla(trans_in))


@trans_in_api.route('/remove/<int:glob_product_id>',
                    methods=['GET'])
@trans_in_api.route('/remove/<int:glob_product_id>/amount/<int:amount>',
                    methods=['GET'])
def remove_from_stock(glob_product_id, amount=1):
    """Get trans_in item."""
    i = 0

    for x in xrange(0, amount):
        trans_in_succes = TransInController.remove_from_stock(glob_product_id)

        print "test1"

        if not trans_in_succes:
            print "neuuu"
            i += 1

    return jsonify(error=str(amount - i) + ' item(s) removed, empty stock',
                   amount=amount - i), 500

    return jsonify(succes='Item removed from stock'), 200


@trans_in_api.route('/all', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_all():
    """Get trans_in item."""
    trans_in_list = TransInController.get_all()

    if not trans_in_list:
        return jsonify(error='Transaction-in items not found'), 500

    return jsonify(trans_in=serialize_sqla(trans_in_list))
