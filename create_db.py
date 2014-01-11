"""create_db.py - Initialize the database.

This script removes any existing databases (brainwave/*.sqlite and brainwave/*.db). It then
uses SQLAlchemy to create tables for all models in the application.

"""
from brainwave import db
from brainwave.models import *
import os
from glob import glob

filelist = glob("brainwave/*.sqlite")
filelist += (glob("brainwave/*.db"))
for f in filelist:
    os.remove(f)

db.create_all()

# Dummy product categories
product_category1 = ProductCategory('Bier')
product_category2 = ProductCategory('Wijn')
db.session.add(product_category1)
db.session.add(product_category2)
db.session.commit()

# Dummy users
user1 = User('Fokke', 'RETARD', 'Fokke Dekker')
user2 = User('Jonas', 'RETARD', 'Jonas Lodewegen')
db.session.add(user1)
db.session.add(user2)
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