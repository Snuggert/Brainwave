"""fill_db.py - Fill the database.

This script fills the database with dummy data, which makes it easier to test
the system.

"""
from brainwave import db
from brainwave.models import *
from werkzeug.security import generate_password_hash
from brainwave.controllers import AssociationController
from brainwave.controllers import CustomerController
# Dummy association
assoc1 = AssociationController.create({'name': 'via', 'login_name': 'via',
                                       'password': 'via',
                                       'email': 'bestuur@svia.nl'})
assoc2 = AssociationController.create({'name': 'House Stark', 'login_name': 'Stark',
                                       'password': 'Winter is Coming',
                                       'email': 'info@stark.sk'})
assoc3 = AssociationController.create({'name': 'House Baratheon', 'login_name': 'Baratheon',
                                       'password': 'Ours is the Fury',
                                       'email': 'info@baratheon.sk'})
assoc4 = AssociationController.create({'name': 'House Lannister', 'login_name': 'Lannister',
                                       'password': 'Hear Me Roar!',
                                       'email': 'info@lannister.sk'})
assoc5 = AssociationController.create({'name': 'nsa', 'login_name': 'nsa',
                                       'password': 'nsa',
                                       'email': 'bla@nsa.nl'})

db.session.add(assoc1)
db.session.add(assoc2)
db.session.add(assoc3)
db.session.add(assoc4)
db.session.add(assoc5)
db.session.commit()

# Dummy customer
AssociationController.set_cash_counter(assoc1, 10)
AssociationController.change_cash_counter(assoc2, 50)


custo1 = Customer('Bas van den Heuvel', "klaplong", "bas@bas.nl", "basklaplong")
db.session.add(custo1)
custo2 = Customer('Jon Snow', 'ghost', "jon@snow.sk", "jonsnow")
db.session.add(custo2)
custo3 = Customer('Joffrey Baratheon', "joffrey", "joffrey@baratheon.sk", "king")
db.session.add(custo3)
custo4 = Customer('Sansa Stark', "sansa", "sansa@stark.sk", "sansa")
db.session.add(custo4)
custo5 = Customer('Maester Luwin')
custo6 = Customer('Barristan Selmy')
custo7 = Customer('Grey Worm')
custo8 = Customer('Mace Tyrell')
custo9 = Customer('Measter Aemon')
custo10 = Customer('Ned Stark')
db.session.add(custo4)
db.session.add(custo5)
db.session.add(custo6)
db.session.add(custo7)
db.session.add(custo8)
db.session.add(custo9)
db.session.add(custo10)
custo11 = Customer('Rob Stark')
db.session.add(custo11)
custo12 = Customer('Jamie Lannister')
db.session.add(custo12)
custo13 = Customer('Jaap Koetsier', 'jaap', 'mail@jkoetsier.nl', 'jaap')
db.session.add(custo13)
custo14 = Customer('Bram van den Akker')
db.session.add(custo14)
custo15 = Customer('Mats ten Bohme')
db.session.add(custo15)
custo16 = Customer('Stein van Zwoll')
db.session.add(custo16)
db.session.commit()

CustomerController.add_association(custo1, assoc1)
CustomerController.add_association(custo1, assoc2)
CustomerController.add_association(custo3, assoc3)
CustomerController.add_association(custo4, assoc2)
CustomerController.add_association(custo10, assoc2)
CustomerController.add_association(custo11, assoc2)
CustomerController.add_association(custo12, assoc4)
CustomerController.add_association(custo13, assoc1)
CustomerController.add_association(custo14, assoc1)
CustomerController.add_association(custo15, assoc1)
CustomerController.add_association(custo16, assoc1)

# Dummy product categories
product_category1 = ProductCategory('Bier', 'FFFFFF', 1)
product_category2 = ProductCategory('Wijn', 'FFFFFF', 1)
product_category3 = ProductCategory('Hartig', 'FFFFFF', 1)
product_category4 = ProductCategory('Frisdrank', 'FFFFFF', 1)
product_category5 = ProductCategory('Snoep', 'FFFFFF', 1)
product_category6 = ProductCategory('Overig', 'FFFFFF', 1)
db.session.add(product_category1)
db.session.add(product_category2)
db.session.add(product_category3)
db.session.add(product_category4)
db.session.add(product_category5)
db.session.add(product_category6)
db.session.commit()

product_category7 = ProductCategory('Bier', 'FFFFFF', 2)
product_category8 = ProductCategory('Wijn', 'FFFFFF', 2)
product_category9 = ProductCategory('Hartig', 'FFFFFF', 2)
product_category10 = ProductCategory('Frisdrank', 'FFFFFF', 2)
product_category11 = ProductCategory('Snoep', 'FFFFFF', 2)
product_category12 = ProductCategory('Overig', 'FFFFFF', 2)
db.session.add(product_category7)
db.session.add(product_category8)
db.session.add(product_category9)
db.session.add(product_category10)
db.session.add(product_category11)
db.session.add(product_category12)
db.session.commit()

# Dummy users
user = User('pietje', generate_password_hash('lalala'), 'lala@lala.la', 1)
db.session.add(user)
db.session.commit()

user = User('admin', generate_password_hash('1234'), 'bladie@bla.nl', 8)
db.session.add(user)
db.session.commit()

# Dummy stock
stock1 = Stock('Hertog Jan', assoc1)
stock2 = Stock('Pinda zakjes', assoc1)
stock3 = Stock('Blikjes cola', assoc1)
stock4 = Stock('Blikjes cola light', assoc1)
stock5 = Stock('Twix', assoc1)
stock6 = Stock('Mars', assoc1)
stock7 = Stock('Blikjes fanta', assoc1)
stock8 = Stock('Blikjes Nestea', assoc1)
stock9 = Stock('Intangibles', assoc1)
stock11 = Stock('Chardonnay', assoc1)
stock12 = Stock('Blikjes fanta', assoc2)
stock13 = Stock('Blikjes Nestea', assoc2)
stock14 = Stock('Intangibles', assoc2)

db.session.add(stock1)
db.session.add(stock2)
db.session.add(stock3)
db.session.add(stock4)
db.session.add(stock5)
db.session.add(stock6)
db.session.add(stock7)
db.session.add(stock8)
db.session.add(stock9)
db.session.add(stock11)
db.session.add(stock12)
db.session.add(stock13)
db.session.add(stock14)
db.session.commit()

# Dummy products
product1 = Product('Hertog Jan 30cL', 'HJ 30cL', 0.70, 30, 'cL', False,
                   product_category1, stock1, assoc1)
product2 = Product('Hertog Jan 50cL', 'HJ 50cL', 1.00, 50, 'cL', False,
                   product_category1, stock1, assoc1)
product3 = Product('Chardonnay 25cL', 'Chard. 25cL', 2.00, 25, 'cL', False,
                   product_category8, stock11, assoc2)
product4 = Product('Zakje pinda\'s', 'Pinda\'s', 1.25, 1, 'amount', True,
                   product_category3, stock2, assoc1)
product5 = Product('Coca Cola 33cL', 'Cola', 0.50, 1, 'amount', True,
                   product_category10, stock3, assoc2)
product6 = Product('Coca Cola Light 33cL', 'Cola L.', 0.50, 1, 'amount', True,
                   product_category4, stock4, assoc1)
product7 = Product('Twix', 'Twix', 0.75, 1, 'amount', True, product_category5,
                   stock5, assoc1)
product8 = Product('Mars', 'Mars', 0.75, 1, 'amount', True, product_category11,
                   stock6, assoc2)
product9 = Product('Fanta 33cL', 'Fanta', 0.50, 1, 'amount', True,
                   product_category4, stock7, assoc1)
product10 = Product('Nestea 33cL', 'Nestea', 0.50, 1, 'amount', True,
                    product_category10, stock8, assoc2)
product11 = Product('Add Credit', 'Credit', 1.00, 0, 'amount', False,
                    product_category6, stock9, assoc1)
product12 = Product('Cash Back', 'Cash', 1.00, 0, 'amount', False,
                    product_category6, stock9, assoc1)
# product13 = Product('Add Credit', 'Credit', 1.00, 0, 'amount',
#                     product_category6, stock9, assoc2)
# product14 = Product('Cash Back', 'Cash', 1.00, 0,
#                     'amount', product_category6, stock9, assoc2)

product15 = Product('Hertog Jan fust leeg', 'HJ -1', 0.0, 1, 'amount', True,
                    product_category6, stock1, assoc1)
product16 = Product('Fles Chardonnay leeg', 'Chard -1', 0.0, 1, 'amount', True,
                    product_category6, stock11, assoc1)

db.session.add(product1)
db.session.add(product2)
db.session.add(product3)
db.session.add(product4)
db.session.add(product5)
db.session.add(product6)
db.session.add(product7)
db.session.add(product8)
db.session.add(product9)
db.session.add(product10)
db.session.add(product11)
db.session.add(product12)
# db.session.add(product13)
# db.session.add(product14)
db.session.add(product15)
db.session.add(product16)
db.session.commit()

# Dummy transactions
trans1 = Transaction('cash', 'paid', assoc1, custo1)
db.session.add(trans1)
db.session.commit()

trans1_piece1 = TransactionPiece(trans1, product1, 1, product1.price)
db.session.add(trans1_piece1)
db.session.commit()
