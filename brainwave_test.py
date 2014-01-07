import unittest
import os
from glob import glob

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

    def test_user(self):
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


if __name__ == '__main__':
    unittest.main()
