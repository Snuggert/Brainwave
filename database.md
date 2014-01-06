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
* association

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
