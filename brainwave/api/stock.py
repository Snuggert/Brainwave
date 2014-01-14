"""stock.py - Controller for stock."""
from flask import Blueprint, jsonify, request
from brainwave.controllers import StockController
from brainwave.utils import serialize_sqla

stock_api = Blueprint('stock_api', __name__,
                      url_prefix='/api/stock')


@stock_api.route('', methods=['POST'])
def create():
    """Create new stock item."""
    stock_dict = request.json

    stock = StockController.create(stock_dict)

    return jsonify(id=stock.id)


@stock_api.route('/<int:stock_id>/<int:quantity>', methods=['PUT'])
def add(stock_id, quantity):
    """Add items to stock."""
    stock = StockController.get(stock_id)

    if not stock:
        return jsonify(error='Stock item not found'), 500

    stock = StockController.add(stock, quantity)

    return jsonify(quantity=stock.quantity)


@stock_api.route('/<int:stock_id>', methods=['DELETE'])
def delete(stock_id):
    """Delete stock item."""
    stock = StockController.get(stock_id)

    if not stock:
        return jsonify(error='Stock item not found'), 500

    StockController.delete(stock)

    return jsonify()


@stock_api.route('/<int:stock_id>', methods=['GET'])
def get(stock_id):
    """Get stock item."""
    stock = StockController.get(stock_id)

    if not stock:
        return jsonify(error='Stock item not found'), 500

    return jsonify(stock=serialize_sqla(stock))


@stock_api.route('/all', methods=['GET'])
def get_all():
    """ Get all stock items unfiltered """
    stock = StockController.get_all()

    if not stock:
        return jsonify(error='Stock item not found'), 500

    return jsonify(stock=serialize_sqla(stock))


@stock_api.route('/search/', methods=['GET'])  # temp
@stock_api.route('/search/<string:query>', methods=['GET'])
def get_all_from(query=""):
    """ Get all stock objects filter by query """
    if query == "":
        stock = StockController.get_all()
    else:
        stock = StockController.get_all_from(query)
    # stock = StockController.get_all()

    if not stock:
        return jsonify(error='Stock item not found'), 200

    return jsonify(stock=serialize_sqla(stock))
