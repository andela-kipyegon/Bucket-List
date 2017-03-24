import json
import unittest

from models import Users, BucketList, BucketListItem
from app import db
from tests.base import BaseTestCase, login_user

class BucketListItemTestCase(BaseTestCase):
    """
    class for the test case BucketListItemAPI
    """

    def create_bucketlist(self):
        """
        fxn that creates a bucketlist
        """

        url = 'api/v1/bucketlist/'
        response = self.client.post(url, data=json.dumps(dict(name='test')),\
                                                headers=self.set_header())
        return response

    def test_create_bucketlist_item(self):
        """
        tests fxn that creates bucketlist
        """

        response = self.create_bucketlist()
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list created successfully')
        url = 'api/v1/bucketlist/1/bucketlistitem'
        response = self.client.post(url, data=json.dumps(dict(item_name='mock')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'item successfully added')

    def test_create_existing_item(self):
        """
         tests fxn create if it can add an existing item
        """

        response = self.create_bucketlist()
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list created successfully')
        url = 'api/v1/bucketlist/1/bucketlistitem'
        response = self.client.post(url, data=json.dumps(dict(item_name='mock')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'item successfully added')
        response = self.client.post(url, data=json.dumps(dict(item_name='mock')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'item already exists')

    def test_update_item(self):
        """
        test fxn  to update a bucketlist item
        """

        response = self.create_bucketlist()
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list created successfully')
        url = 'api/v1/bucketlist/1/bucketlistitem'
        response = self.client.post(url, data=json.dumps(dict(item_name='mocking')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'item successfully added')
        url = 'api/v1/bucketlist/1/bucketlistitem/1'
        response = self.client.put(url, data=json.dumps(dict(item_name='functional testing')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list item is updated')

    def test_update_non_existant_item(self):
        """
         test fxn update if it updates non existant bucketlist item
        """

        response = self.create_bucketlist()
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list created successfully')
        url = 'api/v1/bucketlist/1/bucketlistitem'
        response = self.client.post(url, data=json.dumps(dict(item_name='mocking')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'item successfully added')
        url = 'api/v1/bucketlist/1/bucketlistitem/1'
        response = self.client.put(url, data=json.dumps(dict(item_name='functional testing')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list item is updated')

    def test_delete_item(self):
        """
        test  delete bucketlist item
        """
        
        response = self.create_bucketlist()
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list created successfully')
        url = 'api/v1/bucketlist/1/bucketlistitem'
        response = self.client.post(url, data=json.dumps(dict(item_name='mocking')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'item successfully added')
        url = 'api/v1/bucketlist/1/bucketlistitem/1'
        response = self.client.delete(url, headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list item deleted')

    def test_delete_non_existing_item(self):
        """
        test if can delete a non existant bucket list item
        """

        response = self.create_bucketlist()
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list created successfully')
        url = 'api/v1/bucketlist/1/bucketlistitem'
        response = self.client.post(url, data=json.dumps(dict(item_name='mocking')),\
                                                headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'item successfully added')
        url = 'api/v1/bucketlist/1/bucketlistitem/2'
        response = self.client.delete(url, headers=self.set_header())
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == 'bucket list item does not exist')

        