"""fill_db.py - Fill the database.

This script fills the database with dummy data, which makes it easier to test
the system.

"""
from brainwave import db
from brainwave.models import *

# Dummy product categories
product_category1 = ProductCategory('Bier')
product_category2 = ProductCategory('Wijn')
db.session.add(product_category1)
db.session.add(product_category2)
db.session.commit()

# Dummy users
assoc1 = Association('Fokke', 'RETARD', 'Fokke Dekker')
assoc2 = Association('Jonas', 'RETARD', 'Jonas Lodewegen')
db.session.add(assoc1)
db.session.add(assoc2)
db.session.commit()

# Dummy stock
stock1 = Stock(10000, 'Hertog Jan')
db.session.add(stock1)
db.session.commit()

# Dummy trans_in
trans_in1 = TransIn(100.50, 10000, stock1)
db.session.add(trans_in1)
db.session.commit()

# Dummy products
product1 = Product('Hertog Jan 30cL', 'HJ 30cL', 0.70, 300, product_category1,
                   stock1)
product2 = Product('Hertog Jan 50cL', 'HJ 50cL', 1.00, 500, product_category1,
                   stock1)
db.session.add(product1)
db.session.add(product2)
db.session.commit()
