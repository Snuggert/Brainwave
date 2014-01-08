import unittest
import os
from glob import glob

from flask import json, url_for

from brainwave import app, db
from brainwave.models import *
from brainwave.api.user import UserAPI


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
        assert user.id

        user_dict = user.to_dict()
        new_name = 'Test de Test2'
        user_dict['name'] = new_name
        user = UserAPI.update(user_dict)
        assert user.name == new_name

        user_id = user.id
        user = UserAPI.get(user_id)
        assert user
        assert user.id == user_id

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
        pass

    def test_stock_controller(self):
        pass

if __name__ == '__main__':
    unittest.main()
