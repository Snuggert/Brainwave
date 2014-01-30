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
assoc2 = AssociationController.create({'name': 'nsa', 'login_name': 'nsa',
                                       'password': 'nsa',
                                       'email': 'bla@nsa.nl'})

# Dummy customer
custo1 = Customer('Bas van den Heuvel', "Klaplong", "bas@bas.nl", "basklaplong")
db.session.add(custo1)
custo2 = Customer('Jon Snow')
db.session.add(custo2)
custo3 = Customer('Joffrey Baratheon')
db.session.add(custo3)
custo4 = Customer('Sansa Stark')
db.session.add(custo4)
custo5 = Customer('Maester Luwin')
db.session.add(custo5)
custo6 = Customer('Barristan Selmy')
db.session.add(custo6)
custo7 = Customer('Grey Worm')
db.session.add(custo7)
custo8 = Customer('Mace Tyrell')
db.session.add(custo8)
custo9 = Customer('Measter Aemon')
db.session.add(custo9)
custo10 = Customer('Jaap Koetsier', 'jaap', 'mail@jkoetsier.nl', 'jaap')
db.session.add(custo10)
db.session.commit()

CustomerController.add_association(custo1, assoc1)

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

# Dummy users
user = User('pietje', generate_password_hash('lalala'), 'lala@lala.la', 1)
db.session.add(user)
db.session.commit()

user = User('admin', generate_password_hash('1234'), 'bladie@bla.nl', 8)
db.session.add(user)
db.session.commit()

# Dummy stock
stock1 = Stock('Hertog Jan', False, assoc1)
stock2 = Stock('Pinda zakjes', True, assoc1)
stock3 = Stock('Blikjes cola', True, assoc1)
stock4 = Stock('Blikjes cola light', True, assoc1)
stock5 = Stock('Twix', True, assoc1)
stock6 = Stock('Mars', True, assoc1)
stock7 = Stock('Blikjes fanta', True, assoc1)
stock8 = Stock('Blikjes Nestea', True, assoc1)
stock9 = Stock('Intangibles', True, assoc1)
stock11 = Stock('Chardonnay', False, assoc1)
stock12 = Stock('Blikjes fanta', True, assoc2)
stock13 = Stock('Blikjes Nestea', True, assoc2)
stock14 = Stock('Intangibles', True, assoc2)


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
db.session.commit()

# Dummy products
product1 = Product('Hertog Jan 30cL', 'HJ 30cL', 0.70, 30, 'cL',
                   product_category1, stock1, assoc1)
product2 = Product('Hertog Jan 50cL', 'HJ 50cL', 1.00, 50, 'cL',
                   product_category1, stock1, assoc1)
product3 = Product('Chardonnay 25cL', 'Chard. 25cL', 2.00, 25, 'cL',
                   product_category2, stock11, assoc2)
product4 = Product('Zakje pinda\'s', 'Pinda\'s', 1.25, 1, 'amount',
                   product_category3, stock2, assoc1)
product5 = Product('Coca Cola 33cL', 'Cola', 0.50, 1, 'amount',
                   product_category4, stock3, assoc2)
product6 = Product('Coca Cola Light 33cL', 'Cola L.', 0.50, 1, 'amount',
                   product_category4, stock4, assoc1)
product7 = Product('Twix', 'Twix', 0.75, 1, 'amount', product_category5,
                   stock5, assoc1)
product8 = Product('Mars', 'Mars', 0.75, 1, 'amount', product_category5,
                   stock6, assoc2)
product9 = Product('Fanta 33cL', 'Fanta', 0.50, 1, 'amount', product_category4,
                   stock7, assoc1)
product10 = Product('Nestea 33cL', 'Nestea', 0.50, 1, 'amount',
                    product_category4, stock8, assoc2)
product11 = Product('Add Credit', 'Credit', 1.00, 0, 'amount',
                    product_category6, stock9, assoc1)
product12 = Product('Cash Back', 'Cash', 1.00, 0,
                    'amount', product_category6, stock9, assoc1)
product13 = Product('Add Credit', 'Credit', 1.00, 0, 'amount',
                    product_category6, stock9, assoc2)
product14 = Product('Cash Back', 'Cash', 1.00, 0,
                    'amount', product_category6, stock9, assoc2)

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
db.session.commit()

# Dummy transactions
trans1 = Transaction('cash', 'paid', assoc1, custo1)
db.session.add(trans1)
db.session.commit()

trans1_piece1 = TransactionPiece(trans1, product1, 1, product1.price)
db.session.add(trans1_piece1)
db.session.commit()
