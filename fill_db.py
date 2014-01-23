"""fill_db.py - Fill the database.

This script fills the database with dummy data, which makes it easier to test
the system.

"""
from brainwave import db
from brainwave.models import *
from werkzeug.security import generate_password_hash
from brainwave.controllers import AssociationController

# Dummy association
assoc1 = AssociationController.create({'name': 'via', 'login_name': 'via',
                                       'password': 'via',
                                       'email': 'bestuur@svia.nl'})

# Dummy customer
custo1 = Customer('Bas van den Heuvel')
db.session.add(custo1)

# Dummy product categories
product_category1 = ProductCategory('Bier')
product_category2 = ProductCategory('Wijn')
product_category3 = ProductCategory('Hartig')
product_category4 = ProductCategory('Frisdrank')
product_category5 = ProductCategory('Snoep')
product_category6 = ProductCategory('Overig')
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
stock1 = Stock('Hertog Jan', 10000, assoc1)
db.session.add(stock1)
db.session.commit()

# Dummy trans_in
trans_in1 = TransIn(100.50, 10000, stock1)
db.session.add(trans_in1)
db.session.commit()

# Dummy products
product1 = Product('Hertog Jan 30cL', 'HJ 30cL', 0.70, 300, product_category1,
                   stock1, assoc1)
product2 = Product('Hertog Jan 50cL', 'HJ 50cL', 1.00, 500, product_category1,
                   stock1, assoc1)
product3 = Product('Chardonnay 25cL', 'Chard. 25cL', 2.00, 250, product_category2,
                   stock1, assoc1)
product4 = Product('Zakje pinda\'s', 'Pinda\'s', 1.25, 100, product_category3,
                   stock1, assoc1)
product5 = Product('Coca Cola 33cL', 'Cola', 0.50, 330, product_category4,
                   stock1, assoc1)
product6 = Product('Coca Cola Light 33cL', 'Cola L.', 0.50, 330, product_category4,
                   stock1, assoc1)
product7 = Product('Twix', 'Twix', 0.75, 120, product_category5,
                   stock1, assoc1)
product8 = Product('Mars', 'Mars', 0.75, 120, product_category5,
                   stock1, assoc1)
product9 = Product('Fanta 33cL', 'Fanta', 0.50, 330, product_category4,
                   stock1, assoc1)
product10 = Product('Nestea 33cL', 'Nestea', 0.50, 330, product_category4,
                    stock1, assoc1)
product11 = Product('Toiletpapier (8 velletjes)', 'WC papier', 1.00, 16,
                    product_category6, stock1, assoc1)
product12 = Product('Telefoonkaart', 'Phonecard', 1.00, 500, product_category6,
                    stock1, assoc1)

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
trans1 = Transaction('cash', 'paid', assoc1)
db.session.add(trans1)
db.session.commit()

trans1_piece1 = TransactionPiece(trans1, product1, product1.price, 'sell')
db.session.add(trans1_piece1)
db.session.commit()
