"""stock.py - Controller for stock."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import StockController, TransInController
from brainwave.utils import serialize_sqla
from brainwave.controllers.authentication import Authentication
from brainwave.models import User

stock_api = Blueprint('stock_api', __name__,
                      url_prefix='/api/stock')


@stock_api.route('', methods=['POST'])
@Authentication(User.ROLE_ASSOCIATION)
def create():
    """Create new stock item."""
    stock_dict = request.json
    print stock_dict
    stock = StockController.create(stock_dict)

    return jsonify(id=stock.id)


@stock_api.route('/<int:stock_id>', methods=['PUT'])
@Authentication(User.ROLE_ASSOCIATION)
def update(stock_id):
    """Add items to stock."""
    stock_dict = request.json
    try:
        StockController.update(stock_dict)
    except StockController.NoNameGiven as e:
        return jsonify(error=e.error), 500

    return jsonify()


@stock_api.route('/<int:stock_id>', methods=['DELETE'])
@Authentication(User.ROLE_ASSOCIATION)
def delete(stock_id):
    """Delete stock item."""
    stock = StockController.get(stock_id)

    if not stock:
        return jsonify(error='Stock item not found'), 500

    StockController.delete(stock)

    return jsonify()


@stock_api.route('/<int:stock_id>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get(stock_id):
    """Get stock item."""
    stock = StockController.get(stock_id)

    if not stock:
        return jsonify(error='Stock item not found'), 500

    return jsonify(stock=serialize_sqla(stock))


@stock_api.route('/all', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_all():
    """ Get all stock items unfiltered """
    stocks = StockController.get_all()

    if not stocks:
        return jsonify(stocks=[])

    return jsonify(stocks=serialize_sqla(stocks))


@stock_api.route('/search/', methods=['GET'])  # temp
@stock_api.route('/search/<string:query>', methods=['GET'])
@Authentication(User.ROLE_ASSOCIATION)
def get_all_from(query=""):
    """ Get all stock objects filter by query """
    stock = TransInController.get_all_merged(query)
    # stock = StockController.get_all()
    print stock

    if not stock:
        return jsonify(error='Stock item not found'), 200

    return jsonify(stock=serialize_sqla(stock))
