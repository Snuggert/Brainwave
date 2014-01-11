import unittest
import os
from glob import glob
from flask import json

from brainwave import app, db
from brainwave.models import *
from brainwave.api import *


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

    def test_user_api(self):
        password = 'test1234'
        user_dict = {'username': 'test', 'password': password,
                     'name': 'Test de Test'}
        user = UserAPI.create(user_dict)
        assert user['id']

        user_dict = user
        new_name = 'Test de Test2'
        user_dict['name'] = new_name
        user = UserAPI.update(user_dict)
        assert user['name'] == new_name

        user_id = user['id']
        user = UserAPI.get(user_id)
        assert user
        assert user['id'] == user_id

        assert UserAPI.check_password(user, password)

        UserAPI.delete(user)
        assert not UserAPI.get(user_id)

    def test_user_controller(self):
        with app.test_client() as c, app.app_context():
            password = 'test1234'
            user_dict = {'username': 'test', 'password': password,
                         'name': 'Test de Test'}
            resp = c.post('/api/user', content_type='application/json',
                          data=json.dumps(user_dict))
            data = json.loads(resp.data)
            assert 'id' in data
            assert 'pw_hash' in data

            user_id = data['id']

            new_name = 'Test de Test2'
            user_dict['name'] = new_name
            resp = c.put('/api/user/%d' % (user_id),
                         content_type='application/json',
                         data=json.dumps(user_dict))
            data = json.loads(resp.data)
            assert 'pw_hash' in data

            resp = c.get('/api/user/%d' % (user_id))
            data = json.loads(resp.data)
            assert 'user' in data
            assert data['user']['id'] == user_id

            resp = c.delete('/api/user/%d' % (user_id))
            resp = c.get('/api/user/%d' % (user_id))
            data = json.loads(resp.data)
            assert not 'user' in data

    def test_stock_api(self):
        stock_dict = {'name': 'Hertog Jan fust', 'quantity': 30}
        stock = StockAPI.create(stock_dict)
        assert stock['id']

        stock_dict = {'name': 'Jupiler fust'}
        stock = StockAPI.create(stock_dict)
        assert stock['quantity'] == 0
        stock_id = stock['id']

        StockAPI.add(stock, 2)
        assert stock['quantity'] == 2

        stock2 = StockAPI.get(stock_id)
        assert stock2['name']
        stockall = StockAPI.get_all()
        assert stockall
        stock3 = StockAPI.get(stock_id)
        StockAPI.delete(stock3)
        assert not StockAPI.get(stock_id)

    def test_stock_controller(self):
        with app.test_client() as c, app.app_context():
            stock_dict = {'name': 'Hertog Jan fust', 'quantity': 30}

            resp = c.post('/api/stock', content_type='application/json',
                          data=json.dumps(stock_dict))
            data = json.loads(resp.data)

            assert 'id' in data
            assert 'name' in data
            assert 'quantity' in data

            stock_id = data['id']
            quantity_before = data['quantity']
            quantity_after = quantity_before + 2

            resp = c.put('/api/stock/%d/%d' % (stock_id, 2),
                         content_type='application/json')
            data = json.loads(resp.data)

            assert data['quantity'] == quantity_after

            resp = c.get('/api/stock/%d' % (stock_id),
                         content_type='application/json')
            data = json.loads(resp.data)

            assert 'stock' in data
            assert data['stock']['quantity'] == quantity_after

            resp = c.delete('/api/stock/%d' % (stock_id))
            resp = c.get('/api/stock/%d' % (stock_id),
                         content_type='application/json')
            data = json.loads(resp.data)

            assert not 'stock' in data

    def test_trans_in_api(self):
        stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
        stock = StockAPI.create(stock_dict)
        trans_in_dict = {'price': 100.0, 'volume': 30, 'stock_id': stock['id']}
        trans_in = TransInAPI.create(trans_in_dict)
        assert trans_in['id']

        stock = StockAPI.get(stock['id'])
        assert stock['quantity'] == 60

        trans_in_id = trans_in['id']

        trans_in = TransInAPI.get(trans_in_id)
        assert trans_in['volume'] == 30

        trans_all = TransInAPI.get_all()
        assert trans_all

        TransInAPI.delete(trans_in)
        assert not TransInAPI.get(trans_in_id)

    def test_trans_in_controller(self):
        with app.test_client() as c, app.app_context():
            stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
            stock = StockAPI.create(stock_dict)
            trans_in_dict = {'price': 100.0, 'volume': 30,
                             'stock_id': stock['id']}

            resp = c.post('/api/trans_in', content_type='application/json',
                          data=json.dumps(trans_in_dict))
            data = json.loads(resp.data)

            assert 'id' in data
            assert 'price' in data
            assert 'volume' in data

            trans_in_id = data['id']

            resp = c.get('/api/trans_in/%d' % (trans_in_id),
                         content_type='application/json')
            data = json.loads(resp.data)
            assert data['trans_in']['id'] == trans_in_id

            resp = c.delete('/api/trans_in/%d' % (trans_in_id))
            resp = c.get('/api/trans_in/%d' % (trans_in_id),
                         content_type='application/json')
            data = json.loads(resp.data)

            assert not 'id' in data

    def test_product_category_api(self):
        product_category_dict = {'name': 'bier'}
        product_category = ProductCategoryAPI.create(product_category_dict)
        assert product_category['id']
        assert product_category['name'] == 'bier'

        product_category_id = product_category['id']

        product_category = ProductCategoryAPI.get(product_category_id)
        assert product_category['id'] == product_category_id
        assert product_category['name'] == 'bier'

        product_categories = ProductCategoryAPI.get_all()
        assert product_categories

        ProductCategoryAPI.delete(product_category)
        assert not ProductCategoryAPI.get(product_category_id)

    def test_product_category_controller(self):
        with app.test_client() as c, app.app_context():
            product_category_dict = {'name': 'bier'}
            resp = c.post('/api/product_category',
                          content_type='application/json',
                          data=json.dumps(product_category_dict))
            data = json.loads(resp.data)

            assert 'id' in data
            assert 'name' in data

            product_category_id = data['id']

            resp = c.get('/api/product_category/%d' % (product_category_id),
                         content_type='application/json')
            data = json.loads(resp.data)
            assert data['product_category']['id'] == product_category_id

            resp = c.delete('/api/product_category/%d' % (product_category_id))
            resp = c.get('/api/product_category/%d' % (product_category_id),
                         content_type='application/json')
            data = json.loads(resp.data)

            assert not 'id' in data


if __name__ == '__main__':
    unittest.main()