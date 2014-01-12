"""create_db.py - Initialize the database.

This script removes any existing databases (brainwave/*.sqlite and
brainwave/*.db). It then uses SQLAlchemy to create tables for all models in the
application.

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
