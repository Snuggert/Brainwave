import unittest
import os
from glob import glob
from flask import json

from brainwave import app, db
from brainwave.controllers import *
from brainwave.models import *
from brainwave.api import *
from brainwave.utils import serialize_sqla


class brainwaveTestCase(unittest.TestCase):
    def create_app(self):
        return app

    def setUp(self):
        filelist = glob("brainwave/*.sqlite")
        filelist += (glob("brainwave/*.db"))
        for f in filelist:
            os.remove(f)

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_customer_controller(self):
        customer_dict = {'name': 'Test de Test'}
        customer = CustomerController.create(customer_dict)
        assert customer.id

        customer_dict = serialize_sqla(customer)
        new_name = 'Test de Test2'
        customer_dict['name'] = new_name
        customer = CustomerController.update(customer_dict)
        assert customer.name == new_name

        customer_id = customer.id
        customer = CustomerController.get(customer_id)
        assert customer
        assert customer.id == customer_id

        # Test association coupling.
        association = Association('via')
        db.session.add(association)
        db.session.commit()
        assert not CustomerController.get_associations(customer).all()
        assert not CustomerController.association_is_coupled(customer,
                                                             association)

        CustomerController.add_association(customer, association)
        assert CustomerController.association_is_coupled(customer, association)
        assert CustomerController.get_associations(customer)\
            .first() == association

        CustomerController.remove_association(customer, association)
        assert not CustomerController.get_associations(customer).all()
        assert not CustomerController.association_is_coupled(customer,
                                                             association)

        AssociationController.delete(association)

        CustomerController.delete(customer)
        assert not CustomerController.get(customer_id)

    def test_customer_api(self):
        with app.test_client() as c, app.app_context():
            customer_dict = {'name': 'Test de Test'}
            resp = c.post('/api/customer', content_type='application/json',
                          data=json.dumps(customer_dict))
            data = json.loads(resp.data)
            assert 'id' in data

            customer_id = data['id']
            customer_dict['id'] = customer_id

            new_name = 'Test de Test2'
            customer_dict['name'] = new_name
            resp = c.put('/api/customer/%d' % (customer_id),
                         content_type='application/json',
                         data=json.dumps(customer_dict))
            data = json.loads(resp.data)

            resp = c.get('/api/customer/%d' % (customer_id))
            data = json.loads(resp.data)
            assert 'customer' in data
            assert data['customer']['id'] == customer_id
            assert data['customer']['name'] == new_name

            # Test association coupling.

            association = Association('via')
            db.session.add(association)
            db.session.commit()

            resp = c.get('/api/customer/association/%d' % (customer_id))
            data = json.loads(resp.data)
            assert 'associations' in data
            assert not data['associations']

            resp = c.post('/api/customer/association/%d' % (customer_id),
                          content_type='application/json',
                          data=json.dumps({'association_id': association.id}))
            data = json.loads(resp.data)
            assert not data

            resp = c.get('/api/customer/association/%d' % (customer_id))
            data = json.loads(resp.data)
            assert 'associations' in data
            assert data['associations'][0]['id'] == association.id

            resp = c.delete('/api/customer/association/%d' % (customer_id),
                            content_type='application/json',
                            data=json.dumps({'association_id':
                                             association.id}))
            data = json.loads(resp.data)
            assert not data

            resp = c.get('/api/customer/association/%d' % (customer_id))
            data = json.loads(resp.data)
            assert 'associations' in data
            assert not data['associations']

            resp = c.delete('/api/customer/%d' % (customer_id))
            resp = c.get('/api/customer/%d' % (customer_id))
            data = json.loads(resp.data)
            assert not 'customer' in data

    # def test_stock_api(self):
    #     stock_dict = {'name': 'Hertog Jan fust', 'quantity': 30}
    #     stock = StockAPI.create(stock_dict)
    #     assert stock.id

    #     stock_dict = {'name': 'Jupiler fust'}
    #     stock = StockAPI.create(stock_dict)
    #     assert stock.quantity == 0
    #     stock_id = stock.id

    #     stock = StockAPI.add(stock, 2)
    #     assert stock.quantity == 2

    #     stock = StockAPI.get(stock_id)
    #     assert stock.name

    #     stocks = StockAPI.get_all()
    #     assert stocks

    #     stock = StockAPI.get(stock_id)
    #     StockAPI.delete(stock)
    #     assert not StockAPI.get(stock_id)

    # def test_stock_controller(self):
    #     with app.test_client() as c, app.app_context():
    #         quantity = 30
    #         stock_dict = {'name': 'Hertog Jan fust', 'quantity': quantity}

    #         resp = c.post('/api/stock', content_type='application/json',
    #                       data=json.dumps(stock_dict))
    #         data = json.loads(resp.data)
    #         assert 'id' in data

    #         stock_id = data['id']
    #         quantity_after = quantity + 2

    #         resp = c.put('/api/stock/%d/%d' % (stock_id, 2),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)
    #         assert data['quantity'] == quantity_after

    #         resp = c.get('/api/stock/%d' % (stock_id),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)
    #         assert 'stock' in data
    #         assert data['stock']['quantity'] == quantity_after

    #         resp = c.delete('/api/stock/%d' % (stock_id))
    #         resp = c.get('/api/stock/%d' % (stock_id),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)
    #         assert not 'stock' in data

    def test_trans_in_api(self):
        stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
        stock = StockAPI.create(stock_dict)

        trans_in_dict = {'price': 100.0, 'volume': 30, 'stock_id': stock.id}
        trans_in = TransInAPI.create(trans_in_dict)
        assert trans_in.id

        stock = StockAPI.get(stock.id)
        assert stock.quantity == 60

        trans_in_id = trans_in.id

        trans_in = TransInAPI.get(trans_in_id)
        assert trans_in.volume == 30

        trans_all = TransInAPI.get_all()
        assert trans_all

        TransInAPI.delete(trans_in)
        assert not TransInAPI.get(trans_in_id)

    # def test_trans_in_controller(self):
    #     with app.test_client() as c, app.app_context():
    #         stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
    #         stock = StockAPI.create(stock_dict)
    #         trans_in_dict = {'price': 100.0, 'volume': 30,
    #                          'stock_id': stock.id}

    #         resp = c.post('/api/trans_in', content_type='application/json',
    #                       data=json.dumps(trans_in_dict))
    #         data = json.loads(resp.data)
    #         assert 'id' in data

    #         trans_in_id = data['id']

    #         resp = c.get('/api/trans_in/%d' % (trans_in_id),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)
    #         assert data['trans_in']['id'] == trans_in_id

    #         resp = c.delete('/api/trans_in/%d' % (trans_in_id))
    #         resp = c.get('/api/trans_in/%d' % (trans_in_id),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)
    #         assert not 'trans_in' in data

    # def test_product_category_api(self):
    #     name = 'bier'
    #     product_category_dict = {'name': name}
    #     product_category = ProductCategoryAPI.create(product_category_dict)
    #     assert product_category.id
    #     assert product_category.name == name

    #     product_category_id = product_category.id

    #     product_category = ProductCategoryAPI.get(product_category_id)
    #     assert product_category.id == product_category_id
    #     assert product_category.name == name

    #     product_categories = ProductCategoryAPI.get_all()
    #     assert product_categories

    #     ProductCategoryAPI.delete(product_category)
    #     assert not ProductCategoryAPI.get(product_category_id)

    # def test_product_category_controller(self):
    #     with app.test_client() as c, app.app_context():
    #         product_category_dict = {'name': 'bier'}
    #         resp = c.post('/api/product_category',
    #                       content_type='application/json',
    #                       data=json.dumps(product_category_dict))
    #         data = json.loads(resp.data)
    #         assert 'id' in data

    #         product_category_id = data['id']

    #         resp = c.get('/api/product_category/%d' % (product_category_id),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)
    #         assert data['product_category']['id'] == product_category_id

    #         resp = c.delete('/api/product_category/%d' %
    #               (product_category_id))
    #         resp = c.get('/api/product_category/%d' % (product_category_id),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)

    #         assert not 'product_category' in data

    # def test_product_api(self):
    #     product_category_dict = {'name': 'bier'}
    #     product_category = ProductCategoryAPI.create(product_category_dict)

    #     stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
    #     stock = StockAPI.create(stock_dict)

    #     product_dict = {'name': 'Hertog Jan 30cl', 'shortname': 'HJ 30cl',
    #                     'price': 1.0, 'volume': 1, 'loss': None,
    #                     'product_category_id': product_category.id,
    #                     'stock_id': stock.id}
    #     product = ProductAPI.create(product_dict)
    #     assert product.id
    #     assert product.name == 'Hertog Jan 30cl'
    #     assert product.shortname == 'HJ 30cl'

    #     product_id = product.id

    #     product = ProductAPI.get(product_id)
    #     assert product.id == product_id
    #     assert product.name == 'Hertog Jan 30cl'

    #     products = ProductAPI.get_all()
    #     assert products

    #     ProductAPI.delete(product)
    #     assert not ProductAPI.get(product_id)

    # def test_product_controller(self):
    #     product_category_dict = {'name': 'bier'}
    #     product_category = ProductCategoryAPI.create(product_category_dict)

    #     stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
    #     stock = StockAPI.create(stock_dict)

    #     with app.test_client() as c, app.app_context():
    #         product_dict = {'name': 'Hertog Jan 30cl',
    #                         'shortname': 'HJ 30cl',
    #                         'price': 1.0, 'volume': 1, 'loss': None,
    #                         'product_category_id': product_category.id,
    #                         'stock_id': stock.id}

    #         resp = c.post('/api/product',
    #                       content_type='application/json',
    #                       data=json.dumps(product_dict))
    #         data = json.loads(resp.data)
    #         assert 'id' in data

    #         product_id = data['id']

    #         resp = c.get('/api/product/%d' % (product_id),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)
    #         assert data['product']['id'] == product_id

    #         resp = c.delete('/api/product/%d' % (product_id))
    #         resp = c.get('/api/product/%d' % (product_id),
    #                      content_type='application/json')
    #         data = json.loads(resp.data)

    #         assert not 'id' in data

    def test_user_controller(self):
        # login_name
        # pw_hash
        # email
        # role

        user_dict = {'login_name': 'test', 'password': 'blala',
                     'email': 'bla@bla.nl'}

        user = UserController.create(user_dict)
        assert user

        user_dict['login_name'] = 'test2'
        user = UserController.update(user_dict)
        assert user.login_name == 'test2'

        user_id = user.id
        user = UserController.get(user_id)
        assert user

        user = UserController.get_by_name('test2')
        assert user

        user = UserController.get_by_email('bla@bla.nl')
        assert user

        user_dict = {'login_name': 'test', 'password': 'blalal',
                     'email': 'bla@bla.nl'}

        with self.assertRaises(UserController.UsernameTaken):
            user = UserController.create(user_dict)

        with self.assertRaises(UserController.PasswordIncorrect):
            user = UserController.login('test', 'blalal', False)

        user = UserController.login('test', 'blala', False)
        assert user

        user_id = user.id
        UserController.delete(user)

        user = UserController.get(user_id)
        assert not user

    def test_user_api(self):
        pass

    def test_association_controller(self):

        # Test customer coupling.
        association = Association('via')  # This can be removed when the rest
                                          # of this test is written.
        customer = Customer('Bas')
        db.session.add(association)
        db.session.add(customer)
        db.session.commit()
        assert not AssociationController.get_customers(association).all()
        assert not AssociationController.customer_is_coupled(association,
                                                             customer)

        AssociationController.add_customer(association, customer)
        assert AssociationController.customer_is_coupled(association, customer)
        assert AssociationController.get_customers(association)\
            .first() == customer

        AssociationController.remove_customer(association, customer)
        assert not AssociationController.get_customers(association).all()
        assert not AssociationController.customer_is_coupled(association,
                                                             customer)

        CustomerController.delete(customer)
        AssociationController.delete(association)  # This can also be removed.

    def test_association_api(self):

        with app.test_client() as c, app.app_context():
            # Test customer coupling.
            association = Association('via')  # This can be removed when the
                                              # rest of this test is written.
            customer = Customer('Bas')
            db.session.add(association)
            db.session.add(customer)
            db.session.commit()

            resp = c.get('/api/association/customer/%d' % (association.id))
            data = json.loads(resp.data)
            assert 'customers' in data
            assert not data['customers']

            resp = c.post('/api/association/customer/%d' % (association.id),
                          content_type='application/json',
                          data=json.dumps({'customer_id': customer.id}))
            data = json.loads(resp.data)
            assert not data

            resp = c.get('/api/association/customer/%d' % (association.id))
            data = json.loads(resp.data)
            assert 'customers' in data
            assert data['customers'][0]['id'] == customer.id

            resp = c.delete('/api/association/customer/%d' % (association.id),
                            content_type='application/json',
                            data=json.dumps({'customer_id': customer.id}))
            data = json.loads(resp.data)
            assert not data

            resp = c.get('/api/association/customer/%d' % (association.id))
            data = json.loads(resp.data)
            assert 'customers' in data
            assert not data['customers']

    def test_transaction_controller(self):
        transaction_dict = {'pay_type': 'cash',
                            'items': [{'product_id': '1', 'action': 'sell'},
                                      {'product_id': '2', 'action': 'sell'}]}

        transaction = TransactionController.create(transaction_dict)
        assert transaction

        TransactionController.set_status(transaction.id, 'cancelled')

        transaction2 = TransactionController.get(transaction.id)
        assert transaction2

    def test_credit_controller(self):
        customer = Customer('Bas')
        association = Association('via')
        db.session.add(customer)
        db.session.add(association)
        db.session.commit()

        CustomerController.add_association(customer, association)

        credit_dict = {'credit': 0.0, 'customer_id': customer.id,
                       'association_id': association.id}
        credit = CreditController.create(credit_dict)
        assert credit
        assert credit.id
        assert credit.credit == 0.0

        credit_id = credit.id

        credit = CreditController.get(credit_id)
        assert credit
        assert credit.id == credit_id

        CreditController.add(credit, 20.0)
        assert credit.credit == 20.0

        CreditController.add(credit, -5.0)
        assert credit.credit == 15.0

        CreditController.delete(credit)
        assert not CreditController.get(credit_id)

        # Cleanup.
        CustomerController.remove_association(customer, association)
        CustomerController.delete(customer)
        AssociationController.delete(customer)

    def test_credit_api(self):
        customer = Customer('Bas')
        association = Association('via')
        db.session.add(customer)
        db.session.add(association)
        db.session.commit()

        CustomerController.add_association(customer, association)

        with app.test_client() as c, app.app_context():
            credit_dict = {'credit': 0.0, 'customer_id': customer.id,
                           'association_id': association.id}
            resp = c.post('/api/credit', content_type='application/json',
                          data=json.dumps(credit_dict))
            data = json.loads(resp.data)
            assert 'id' in data

            credit_id = data['id']
            credit_dict['id'] = credit_id

            resp = c.get('/api/credit/%d' % (credit_id))
            data = json.loads(resp.data)
            assert 'credit' in data
            assert 'id' in data['credit']
            assert data['credit']['id'] == credit_id

            resp = c.post('/api/credit/add/%d' % (credit_id),
                          content_type='application/json',
                          data=json.dumps({'amount': 20.0}))
            data = json.loads(resp.data)
            assert 'new_credit' in data
            assert data['new_credit'] == 20.0

            credit_dict['credit'] = data['new_credit']

            resp = c.post('/api/credit/add/%d' % (credit_id),
                          content_type='application/json',
                          data=json.dumps({'amount': -5.0}))
            data = json.loads(resp.data)
            assert 'new_credit' in data
            assert data['new_credit'] == 15.0

            credit_dict['credit'] = data['new_credit']

            resp = c.delete('/api/credit/%d' % (credit_id))
            data = json.loads(resp.data)
            assert not data

            resp = c.get('/api/credit/%d' % (credit_id))
            data = json.loads(resp.data)
            assert data
            assert 'error' in data
            assert data['error'] == 'Credit not found'

        CustomerController.remove_association(customer, association)
        CustomerController.delete(customer)
        AssociationController.delete(association)

if __name__ == '__main__':
    unittest.main()
