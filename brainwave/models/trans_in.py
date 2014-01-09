"""trans_in.py - TransIn model."""
from brainwave import db
from brainwave.utils.base_model import BaseEntity


class TransIn(db.Model, BaseEntity):
	""""The transaction in Model"""
	__tablename__ = 'trans_in'

	price = db.Column(db.Float)
	volume = db.Column(db.Integer)
	in_stock = db.Column(db.Boolean)

	stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
	def __init__(price=None, volume=None, stock=None):
		self.price = price
		self.volume = volume
		self.stock = stock
