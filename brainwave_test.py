import unittest
import os
from glob import glob
from flask import json

from brainwave import app, db
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

    def test_association_api(self):
        password = 'test1234'
        association_dict = {'login_name': 'test', 'password': password,
                            'name': 'Test de Test'}
        association = AssociationAPI.create(association_dict)
        assert association.id

        association_dict = serialize_sqla(association)
        new_name = 'Test de Test2'
        association_dict['name'] = new_name
        association = AssociationAPI.update(association_dict)
        assert association.name == new_name

        association_id = association.id
        association = AssociationAPI.get(association_id)
        assert association
        assert association.id == association_id

        assert AssociationAPI.check_password(association, password)

        AssociationAPI.delete(association)
        assert not AssociationAPI.get(association_id)

    def test_association_controller(self):
        with app.test_client() as c, app.app_context():
            password = 'test1234'
            association_dict = {'login_name': 'test', 'password': password,
                                'name': 'Test de Test'}
            resp = c.post('/api/association', content_type='application/json',
                          data=json.dumps(association_dict))
            data = json.loads(resp.data)
            assert 'id' in data
            assert 'pw_hash' in data

            association_id = data['id']

            new_name = 'Test de Test2'
            association_dict['name'] = new_name
            resp = c.put('/api/association/%d' % (association_id),
                         content_type='application/json',
                         data=json.dumps(association_dict))
            data = json.loads(resp.data)
            assert 'pw_hash' in data

            resp = c.get('/api/association/%d' % (association_id))
            data = json.loads(resp.data)
            assert 'association' in data
            assert data['association']['id'] == association_id

            resp = c.delete('/api/association/%d' % (association_id))
            resp = c.get('/api/association/%d' % (association_id))
            data = json.loads(resp.data)
            assert not 'association' in data

    def test_stock_api(self):
        stock_dict = {'name': 'Hertog Jan fust', 'quantity': 30}
        stock = StockAPI.create(stock_dict)
        assert stock.id

        stock_dict = {'name': 'Jupiler fust'}
        stock = StockAPI.create(stock_dict)
        assert stock.quantity == 0
        stock_id = stock.id

        stock = StockAPI.add(stock, 2)
        assert stock.quantity == 2

        stock = StockAPI.get(stock_id)
        assert stock.name

        stocks = StockAPI.get_all()
        assert stocks

        stock = StockAPI.get(stock_id)
        StockAPI.delete(stock)
        assert not StockAPI.get(stock_id)

    def test_stock_controller(self):
        with app.test_client() as c, app.app_context():
            quantity = 30
            stock_dict = {'name': 'Hertog Jan fust', 'quantity': quantity}

            resp = c.post('/api/stock', content_type='application/json',
                          data=json.dumps(stock_dict))
            data = json.loads(resp.data)
            assert 'id' in data

            stock_id = data['id']
            quantity_after = quantity + 2

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

    def test_trans_in_controller(self):
        with app.test_client() as c, app.app_context():
            stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
            stock = StockAPI.create(stock_dict)
            trans_in_dict = {'price': 100.0, 'volume': 30,
                             'stock_id': stock.id}

            resp = c.post('/api/trans_in', content_type='application/json',
                          data=json.dumps(trans_in_dict))
            data = json.loads(resp.data)
            assert 'id' in data

            trans_in_id = data['id']

            resp = c.get('/api/trans_in/%d' % (trans_in_id),
                         content_type='application/json')
            data = json.loads(resp.data)
            assert data['trans_in']['id'] == trans_in_id

            resp = c.delete('/api/trans_in/%d' % (trans_in_id))
            resp = c.get('/api/trans_in/%d' % (trans_in_id),
                         content_type='application/json')
            data = json.loads(resp.data)
            assert not 'trans_in' in data

    def test_product_category_api(self):
        name = 'bier'
        product_category_dict = {'name': name}
        product_category = ProductCategoryAPI.create(product_category_dict)
        assert product_category.id
        assert product_category.name == name

        product_category_id = product_category.id

        product_category = ProductCategoryAPI.get(product_category_id)
        assert product_category.id == product_category_id
        assert product_category.name == name

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

            product_category_id = data['id']

            resp = c.get('/api/product_category/%d' % (product_category_id),
                         content_type='application/json')
            data = json.loads(resp.data)
            assert data['product_category']['id'] == product_category_id

            resp = c.delete('/api/product_category/%d' % (product_category_id))
            resp = c.get('/api/product_category/%d' % (product_category_id),
                         content_type='application/json')
            data = json.loads(resp.data)

            assert not 'product_category' in data

    def test_product_api(self):
        product_category_dict = {'name': 'bier'}
        product_category = ProductCategoryAPI.create(product_category_dict)

        stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
        stock = StockAPI.create(stock_dict)

        product_dict = {'name': 'Hertog Jan 30cl', 'shortname': 'HJ 30cl',
                        'price': 1.0, 'volume': 1, 'loss': None,
                        'product_category_id': product_category.id,
                        'stock_id': stock.id}
        product = ProductAPI.create(product_dict)
        assert product.id
        assert product.name == 'Hertog Jan 30cl'
        assert product.shortname == 'HJ 30cl'

        product_id = product.id

        product = ProductAPI.get(product_id)
        assert product.id == product_id
        assert product.name == 'Hertog Jan 30cl'

        products = ProductAPI.get_all()
        assert products

        ProductAPI.delete(product)
        assert not ProductAPI.get(product_id)

    def test_product_controller(self):
        product_category_dict = {'name': 'bier'}
        product_category = ProductCategoryAPI.create(product_category_dict)

        stock_dict = {'name': 'Hertog Jan', 'quantity': 30}
        stock = StockAPI.create(stock_dict)

        with app.test_client() as c, app.app_context():
            product_dict = {'name': 'Hertog Jan 30cl', 'shortname': 'HJ 30cl',
                            'price': 1.0, 'volume': 1, 'loss': None,
                            'product_category_id': product_category.id,
                            'stock_id': stock.id}

            resp = c.post('/api/product',
                          content_type='application/json',
                          data=json.dumps(product_dict))
            data = json.loads(resp.data)
            assert 'id' in data

            product_id = data['id']

            resp = c.get('/api/product/%d' % (product_id),
                         content_type='application/json')
            data = json.loads(resp.data)
            assert data['product']['id'] == product_id

            resp = c.delete('/api/product/%d' % (product_id))
            resp = c.get('/api/product/%d' % (product_id),
                         content_type='application/json')
            data = json.loads(resp.data)

            assert not 'id' in data


if __name__ == '__main__':
    unittest.main()
