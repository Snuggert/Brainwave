"""transaction.py - Controller calls for transaction."""
from flask import session
from brainwave import db
from brainwave.models import Transaction, Association
from brainwave.controllers.transaction_piece import TransactionPieceController
from brainwave.controllers.user import UserController
from brainwave.controllers.product import ProductController
from brainwave.controllers.customer import CustomerController
from brainwave.controllers.credit import CreditController
from brainwave.controllers.stock import StockController

from brainwave import app
import logging


class TransactionController:
    class UnknownError(Exception):
        def __init__(self):
            self.error = 'An unexpected error occurred.'

    class MissingCredit(Exception):
        def __init__(self):
            self.error = 'The customer does not have enough credit!' + \
                         ' Transaction cancelled.'

    class NoCustomerSelected(Exception):
        def __init__(self):
            self.error = 'You must select a customer for this transaction.'

    class NotCoupled(Exception):
        def __init__(self):
            self.error = 'The customer is not a part of this assocation.'

    class BadQuantity(Exception):
        def __init__(self):
            self.error = 'The provided quantity is not valid.'

    class BadProduct(Exception):
        def __init__(self):
            self.error = 'One of the selected products does not exist.'

    @staticmethod
    def create(ta_dict):
        # Temporarily set assoc_id to 1, should be changed later
        transaction = Transaction.new_dict({'assoc_id': '1',
                                            'cust_id': ta_dict['customer_id'],
                                            'pay_type': ta_dict['pay_type'],
                                            'status': 'pending',
                                            'action': ta_dict['action']})

        if not transaction:
            raise TransactionController.UnknownError()

        db.session.add(transaction)
        db.session.commit()

        # Set a variable that is meant to track the total order price
        price_total = 0
        # Set a variable that is set to True when credit is being SOLD
        sell_credit = False

        # purchase is a list that should hold all transaction_pieces and their
        # matching products. As such, it is a list of lists.
        purchase = []
        # Create individual records for each individual "transaction_piece"
        for piece in ta_dict['entries']:
            if piece['quantity'] < 0:
                raise TransactionController.BadQuantity()
            # Add transaction_id to the piece
            piece['transaction_id'] = transaction.id

            # Verify that the product exists (and use it to get the price)
            product = ProductController.get(piece['product_id'])
            if not product:
                raise TransactionController.BadProduct()

            piece['price'] = product.price * piece['quantity']
            price_total += piece['price']

            # Create a new transaction piece
            transaction_piece = TransactionPieceController.create(piece)
            if not transaction_piece:
                raise TransactionController.UnknownError()
            else:
                purchase.append([transaction_piece, product])
                if product.shortname == "Credit":
                    sell_credit = True

        # If the transaction somehow involves credit, make sure that the
        # customers credit object is available. This is needed for regular
        # credit transactions as well as adding credit to the balance (or
        # returning it to the customer)
        if transaction.pay_type == 'credit' or sell_credit is True:
            if not transaction.cust_id:
                raise TransactionController.NoCustomerSelected()

            # Get the association that the barteam is a part of
            user_id = session['user_id']
            user = UserController.get(user_id)
            if not user.association:
                # The bar login team is not coupled to an association?
                raise TransactionController.UnknownError()
            association = user.association[0]

            # Get the customer that was selected for this transaction
            customer = CustomerController.get(transaction.cust_id)
            if not customer or CustomerController.association_is_coupled(
                    customer, association) is False:
                raise TransactionController.NotCoupled()

            # Get the credit object matched to this customer
            credit = customer.credits.filter(Association.id == association.id)\
                .first()

        if transaction.pay_type == 'credit':
            # Make sure the customer has enough credit
            if credit.credit < price_total:
                raise TransactionController.MissingCredit()
            else:
                # Subtract the costs by adding a negative amount
                CreditController.add(credit, price_total * -1)

        # Now iterate the individual parts of the purchase again, and
        # manipulate stock (or credit) as needed.
        # Note: p[0] is a transaction_piece, p[1] is a product
        for p in purchase:
            if p[1].shortname == "Cash":
                pass  # When implemented, update the cash counter.
            elif p[1].shortname == "Credit":
                # Customer wants to buy credit, so add it to his balance.
                CreditController.add(credit, p[0].price)
            elif p[1].stock.direct:
                # Manipulate the stock for this particular product here
                StockController.remove(p[1].stock, p[0].quantity)
            else:
                pass

        # Finally, update the status of the transaction to "paid"
        TransactionController.set_status(transaction.id, 'paid')

        return transaction

    @staticmethod
    def get(transaction_id):
        """ Get a Transaction object by its id """

        return Transaction.query.get(transaction_id)

    @staticmethod
    def get_between(date_1, date_2):
        """ Get a Transaction objects between date_1 and date_2 """
        return Transaction.query.filter(Transaction.created >= date_1).\
            filter(Transaction.created <= date_2).all()

    @staticmethod
    def set_status(transaction_id, status):
        """ Set the status of a transaction """
        Transaction.query.filter_by(id=transaction_id) \
                         .update(dict(status=status))
        db.session.commit()

    @staticmethod
    def get_all():
        """ Get all Transaction objects """

        return Transaction.query.all()
