""" stock.py - Controller for stock. """
from flask import Blueprint, jsonify, request
from brainwave.api.stock import StockAPI
from brainwave.utils import serialize_sqla

stock_controller = Blueprint('stock_controller', __name__,
                             url_prefix='/api/stock')


@stock_controller.route('', methods=['POST'])
def create():
    """ Create new stock item """
    stock_dict = request.json

    stock = StockAPI.create(stock_dict)

    return jsonify(id=stock['id'], name=stock['name'],
                   quantity=stock['quantity'])


@stock_controller.route('/<int:stock_id>/<int:quantity>', methods=['PUT'])
def add(stock_id, quantity):
    """ Add items to stock """
    stock = StockAPI.get(stock_id)

    if not stock:
        return jsonify(error='Stock item not found'), 500

    stock = StockAPI.add(stock, quantity)

    return jsonify(id=stock['id'], name=stock['name'],
                   quantity=stock['quantity'])


@stock_controller.route('/<int:stock_id>', methods=['DELETE'])
def delete(stock_id):
    """ Delete stock item """
    stock = StockAPI.get(stock_id)

    if not stock:
        return jsonify(error='Stock item not found'), 500

    StockAPI.delete(stock)

    return jsonify()


@stock_controller.route('/<int:stock_id>', methods=['GET'])
def get(stock_id):
    """ Get stock item """
    stock = StockAPI.get(stock_id)

    if not stock:
        return jsonify(error='Stock item not found'), 500

    return jsonify(stock=serialize_sqla(stock))