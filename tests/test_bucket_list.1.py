import json
import unittest


from models import Users, BucketList
from app import db
from tests.base import BaseTestCase, login_user

class BucketListTestCase(BaseTestCase):
    """class for the BucketListAPI resource"""

    def create_bucketlist(self):
        """
        method to create a bucketlist for tests
        """

        url = 'api/v1/bucketlist/'
        response = self.client.post(url, data=json.dumps(dict(name='test')),\
                                                headers=self.set_header())
        return response

    def test_create_bucket_list(self):
        """
        test fxn to create a bucketlist
        """

        with self.client:
            response = self.create_bucketlist()
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'test')

    def test_get_bucketlists(self):
        """
        test fxn to get bucketlists
        """

        with self.client:
            response = self.create_bucketlist()
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'test')
            url = 'api/v1/bucketlist/'
            response = self.client.get(url, headers=self.set_header())
            data = json.loads(response.data.decode())
            self.assertTrue(data['bucketlist'][0]['name'] == 'test')

    def test_update_bucketlist(self):
        """
        test fxn to update bucket list
        """

        with self.client:
            response = self.create_bucketlist()
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'test')
            url = 'api/v1/bucketlist/1'
            response = self.client.put(url, data=json.dumps(dict(name='production')),\
                                                       headers=self.set_header())
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'production')

    def test_delete_bucketlist(self):
        """
        test fxn to delete bucketlist
        """

        with self.client:
            response = self.create_bucketlist()
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'test')
            url = 'api/v1/bucketlist/1'
            response = self.client.delete(url, headers=self.set_header())
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'bucket list test deleted successfully')

    def test_existing_bucketlist(self):
        """
        test creating an existing bucket list
        """

        with self.client:
            response = self.create_bucketlist()
            data = json.loads(response.data.decode())
            self.assertTrue(data['name'] == 'test')
            url = 'api/v1/bucketlist/'
            response = self.client.post(url, data=json.dumps(dict(name='test')),\
                                                       headers=self.set_header())
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'bucketlist test already exists')
