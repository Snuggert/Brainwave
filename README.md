Brainwave
=========

Specifications
<<<<<<< HEAD
=========
* Pre-paid Selling
* Modulair screen (scalable)
* Administration
* Inventory
* Api 
* Barteam login / assosiations login
* Two stocks on one tablet
* Utp cassier system
* Beer statistics
* pep8
* Mobile version(?)
* Customer frontend
* 

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
* time
* product
* user_team
* user_assosiations
* user_customer 

### Transaction-in
* Stock_id
* Price
* Volume
* in_stock

* Stock (link, one  to one)


### Team
* Id
* assosiation

### team_member
* team
* user

### users
* Name
* Pin

### Credits
* User
* Amount
* Assosiation

### Members
* Assosiation
* User



#### Libraries
* Flask - http://flask.pocoo.org/ (Webframework)
* Flask-SQLAlchemy - http://pythonhosted.org/Flask-SQLAlchemy/ (SQLAlchemy
integration for Flask)
* Sass - http://sass-lang.com/ (Enhanced css, with things like nesting and
mixins)


