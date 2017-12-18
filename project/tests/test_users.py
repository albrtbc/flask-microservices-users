# project/tests/test_users.py


import json

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email, created_at=datetime.datetime.utcnow()):
    user = User(username=username, email=email, created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='albert',
                        email='albert@rbit.io'
                        )),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('albert@rbit.io was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict()),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a username key."""
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict(email='albert@rbit.io')),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_user_duplicate_user(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='albert',
                        email='albert@rbit.io'
                        )),
                    content_type='application/json',
                    )
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='albert',
                        email='albert@rbit.io'
                        )),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('albert', 'albert@rbit.io')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('albert', data['data']['username'])
            self.assertIn('albert@rbit.io', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        created = datetime.datetime.utcnow() + datetime.timedelta(-30)
        add_user('albert', 'albert@rbit.io', created)
        add_user('fran', 'fran@rbit.io')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('albert', data['data']['users'][0]['username'])
            self.assertIn(
                    'albert@rbit.io', data['data']['users'][0]['email'])
            self.assertIn('fran', data['data']['users'][1]['username'])
            self.assertIn(
                    'fran@rbit.io', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])
