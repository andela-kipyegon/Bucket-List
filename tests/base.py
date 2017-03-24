import os
import json

from flask_testing import TestCase
from app import db, app
from models import Users, BucketList, BucketListItem

def register_user(self, first_name, last_name, email, password):
    return self.client.post(
        'api/v1/auth/register',
        data=json.dumps(dict(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )),
        content_type='application/json',
    )

def login_user(self, email, password):
    return self.client.post(
        'api/v1/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )

class BaseTestCase(TestCase):

    def create_app(self):
        """configure app test settings"""

        app.config.from_object('config.TestingConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        """setup resources for the test"""
        db.create_all()
        register_user(self, 'joe', 'gitau', 'joe@gmail.com', '123456')
        response = login_user(self, 'joe@gmail.com', '123456')
        data = json.loads(response.data.decode())

        self.token = data['auth_token']

    def set_header(self):
        """set header e.g Authorization and Content type"""

        response = login_user(self, 'joe@gmail.com', '123456')
        data = json.loads(response.data.decode())
        self.token = data['auth_token']
        return{'Authorization':'Token ' + self.token,
               'Content-Type': 'application/json',
               'Accept':'application/json',
              }

    def tearDown(self):
        """ removes all tables and removes test db
        """
        db.session.remove()
        db.drop_all()
        os.remove('test.db')
