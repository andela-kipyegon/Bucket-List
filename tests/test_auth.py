import json
import os
import unittest

from base import BaseTestCase, register_user, login_user

class TestAuth(BaseTestCase):
    """Class test case for authentication"""

    def test_register_new_user(self):
        """
        test registration of new user
        """
        with self.client:
            response = register_user(self, 'ken', 'kip', 'kenkip@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)


    def test_register_already_registered_user(self):
        """
        test for already registered
        """
        with self.client:
            response = register_user(self, 'joe', 'gitau', 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """
        test loggin successful after login
        """

        with self.client:
            register_user(self, 'joe', 'gitau', 'joe@gmail.com', '123456')
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_unregistered_user_login(self):
        """
        test if unregistered user can log in
        """

        with self.client:
            response = login_user(self, 'kip@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid user or Password mismatch.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_missing_registration_parameters(self):
        """
        test missing registration parameters
        """
        with self.client:
            response = register_user(self, 'joe', 'gitau', 'dedeee', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['message']['email'] == 'Invalid email')

