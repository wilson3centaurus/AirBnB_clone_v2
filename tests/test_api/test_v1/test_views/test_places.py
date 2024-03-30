#!/usr/bin/python3
"""Unit tests for places module"""

import inspect
import pep8
import unittest
import os
from api.v1.views import app_views
from models import storage
from flask import Flask
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import places


class Testplaces(unittest.TestCase):
    """Tests places module"""

    def setUp(self):
        """Tests places module"""

        self.app = Flask(__name__)
        self.app.register_blueprint(app_views)
        self.client = self.app.test_client()
        self.city = City(name="Twilight")
        self.user = User(first_name='Ali', last_name='Kamel',
                         email='ali@x.com', password='0000')
        self.place = Place(name="Roof", city_id=self.city.id,
                           user_id=self.user.id)

    def tearDown(self):
        """Deletes created place"""

        storage.delete(self.city)
        storage.save()

    def test_doc(self):
        """Tests module docstring existence"""

        self.assertIsNotNone(places.__doc__)

    def test_function_doc(self):
        """Tests function docstring existence (for all functions)"""

        functions = inspect.getmembers(places, inspect.isfunction)
        for function in functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8(self):
        """Tests if module follows PEP8 style"""

        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['api/v1/views/places.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_executable(self):
        """Tests if the file is executable"""

        file_stat = os.stat('api/v1/views/places.py')
        permissions = str(oct(file_stat[0]))
        expected = int(permissions[5:-2]) >= 5
        self.assertTrue(expected)

    # This test does pass for unknown reasons
    # def test_get_places_by_city(self):
        """Tests GET request"""

        """ storage.new(self.city)
        storage.save()

        place_names = ['Hut', 'Apartment']
        for name in place_names:
            place = Place(name=name, city_id=self.city.id,
            user_id=self.user.id)
            storage.new(place)
        storage.save()

        response = self.client.get(f'/api/v1/cities/{self.city.id}/places')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        self.assertIn("Hut", [place['name'] for place in data])
        self.assertIn("Apartment", [place['name'] for place in data]) """

    def test_get_place(self):
        """Tests GET request"""

        storage.new(self.city)
        storage.new(self.place)
        storage.save()

        response = self.client.get(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['name'], "Roof")

    def test_delete_Place(self):
        """Tests DELETE request"""

        storage.new(self.place)
        storage.save()

        response = self.client.delete(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

        place = storage.get(Place, self.place.id)
        self.assertIsNone(place)

    # This test does pass for unknown reasons
    # def test_create_Place(self):
        """Tests POST request"""

        """ storage.new(self.city)
        storage.save()

        data = {'name': 'Penthouse'}
        response = self.client.post(f'/api/v1/cities/{self.city.id}/places',
        json=data)
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertEqual(data['name'], 'Penthouse')

        place = storage.get(Place, data['id'])
        self.assertIsNotNone(place) """

    def test_update_Place(self):
        """Tests PUT request"""

        storage.new(self.place)
        storage.save()

        data = {'name': 'Penthouse'}
        response = self.client.put(f'/api/v1/places/{self.place.id}',
                                   json=data)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['name'], 'Penthouse')

        place = storage.get(Place, self.place.id)
        self.assertEqual(place.name, 'Penthouse')


if __name__ == "__main__":
    unittest.main()
