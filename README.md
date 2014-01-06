Brainwave
=========

bar backend/frontend for the brainwave bar at sciencepark

Products
=========

### Category
* Name

### Product
* Active
* Short name
* Name (immutable)
* Price (immutable)
* Volume (immutable)
* Loss

* Category (link)
* Stock (link, one to one)

### Stock
* Stock
* Type of Stock

* Product (link, one to many) 

### Transaction-out
* 

### Transaction-in
* Quantity
* Price

* Stock (link, one  to one)

#### Libraries
* Flask - http://flask.pocoo.org/ (Webframework)
* Flask-SQLAlchemy - http://pythonhosted.org/Flask-SQLAlchemy/ (SQLAlchemy
integration for Flask)
* Sass - http://sass-lang.com/ (Enhanced css, with things like nesting and
mixins)