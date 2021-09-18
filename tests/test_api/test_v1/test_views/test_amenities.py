#!/usr/bin/python3
import json
from models import storage
from models.amenity import Amenity
from models.state import State
import os
import requests
import unittest


host = os.environ['HBNB_API_HOST']
port = os.environ['HBNB_API_PORT']
version = '/v1'
api_url = 'http://{}:{}/api{}'.format(host, port, version)


WRONG_STATUS_CODE_MSG = 'Wrong status code!'
WRONG_TYPE_RETURN_MSG = 'Wrong return type return!'
WRONG_OBJ_TYPE_MSG = 'Wrong object type!'
MISSING_NAME_ATTR_MSG = 'Missing name!'
MISSING_CREATED_AT_ATTR_MSG = 'Missing created_at!'
MISSING_UPDATED_AT_ATTR_MSG = 'Missing updated_at!'
MISSING_CLASS_ATTR_MSG = 'Missing class!'


class ListAmenitiesApiTest(unittest.TestCase):
    """
        Tests of API list action for Amenity.
    """

    def setUp(self) -> None:
        """
            Set up API list action tests.
        """
        self.url = '{}/amenities'.format(api_url)

    def testList(self):
        """
            Test valid list action.
        """
        response = requests.get(url=self.url)
        headers = response.headers

        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)

    def testCount(self):
        """
            Test list length.
        """
        initial_count = len(storage.all(Amenity))
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

    def testOnlyAmenity(self):
        """
            Test valid list action with Amenity content only.
        """
        state = State(name='toto')
        amenity = Amenity(name='toto')
        storage.new(state)
        storage.new(amenity)
        storage.save()

        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(
                element['__class__'],
                'Amenity',
                WRONG_OBJ_TYPE_MSG
            )

        storage.delete(amenity)
        storage.delete(state)
        storage.save()


class ShowAmenitiesApiTest(unittest.TestCase):
    """
        Tests of API show action for Amenity.
    """

    def setUp(self) -> None:
        """
            Set up API show action tests.
        """
        self.amenity = Amenity(name='toto')
        storage.new(self.amenity)
        storage.save()
        self.url = '{}/amenities/{}'.format(api_url, self.amenity.id)
        self.invalid_url = '{}/amenities/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Amenity of database used for tests.
        """
        storage.delete(self.amenity)
        storage.save()

    def testShow(self):
        """
            Test valid show action.
        """
        response = requests.get(url=self.url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertIn('name', json_data)
        self.assertIn('created_at', json_data)
        self.assertIn('updated_at', json_data)
        self.assertIn('__class__', json_data)
        self.assertEqual(json_data['name'], self.amenity.name)

    def testNotFound(self):
        """
            Test show action when given wrong amenity_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.amenity == storage.get(Amenity, self.amenity.id))
        self.assertEqual(json_data['error'], 'Not found')


class DeleteAmenitiesApiTest(unittest.TestCase):
    """
        Tests of API delete action for Amenity.
    """

    def setUp(self) -> None:
        """
            Set up API delete action tests.
        """
        self.amenity = Amenity(name='toto')
        self.amenity_id = self.amenity.id
        storage.new(self.amenity)
        storage.save()
        self.url = '{}/amenities/{}'.format(api_url, self.amenity_id)
        self.invalid_url = '{}/amenities/{}'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Amenity of database used for tests.
        """
        if storage.get(Amenity, self.amenity_id) is not None:
            storage.delete(self.amenity)
            storage.save()

    def testDelete(self):
        """
            Test valid delete action.
        """
        response = requests.delete(url=self.url)
        headers = response.headers
        json_data = response.json()

        self.assertTrue(self.amenity == storage.get(Amenity, self.amenity_id))
        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertEqual(len(json_data), 0)
        storage.reload()
        self.assertIsNone(storage.get(Amenity, self.amenity_id))

    def testNotFound(self):
        """
            Test delete action when given wrong amenity_id or no ID at all.
        """
        response = requests.delete(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.amenity == storage.get(Amenity, self.amenity_id))
        self.assertEqual(json_data['error'], 'Not found')
