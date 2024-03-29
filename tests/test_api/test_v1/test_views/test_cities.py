#!/usr/bin/python3
"""
Unittests for the view for City objects
- TestCityAPI
"""

import unittest
from flask import Flask
from api.v1.views import app_views
from models import storage, State, City

class TestCityAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(app_views)
        self.client = self.app.test_client()
        self.state = State(name="California")
        self.city = City(name="San Francisco", state_id=self.state.id)

    def tearDown(self):
        storage.delete(self.state)
        storage.save()

    def test_get_cities_by_state(self):
        # Create a state
        storage.new(self.state)
        storage.save()

        # Create cities
        city_names = ["Los Angeles", "San Diego"]
        for name in city_names:
            city = City(name=name, state_id=self.state.id)
            storage.new(city)
        storage.save()

        # Test GET request
        response = self.client.get(f'/api/v1/states/{self.state.id}/cities')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        self.assertIn("Los Angeles", [city['name'] for city in data])
        self.assertIn("San Diego", [city['name'] for city in data])

    def test_get_city(self):
        # Create a state and city
        storage.new(self.state)
        storage.new(self.city)
        storage.save()

        # Test GET request
        response = self.client.get(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['name'], "San Francisco")

    def test_delete_city(self):
        # Create a state and city
        storage.new(self.state)
        storage.new(self.city)
        storage.save()

        # Test DELETE request
        response = self.client.delete(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

        # Make sure the city is deleted
        city = storage.get(City, self.city.id)
        self.assertIsNone(city)

    def test_create_city(self):
        # Create a state
        storage.new(self.state)
        storage.save()

        # Test POST request
        new_city_data = {'name': 'San Jose'}
        response = self.client.post(f'/api/v1/states/{self.state.id}/cities', json=new_city_data)
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertEqual(data['name'], 'San Jose')

        # Make sure the city is created
        city = storage.get(City, data['id'])
        self.assertIsNotNone(city)

    def test_update_city(self):
        # Create a state and city
        storage.new(self.state)
        storage.new(self.city)
        storage.save()

        # Test PUT request
        updated_city_data = {'name': 'Los Angeles'}
        response = self.client.put(f'/api/v1/cities/{self.city.id}', json=updated_city_data)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['name'], 'Los Angeles')

        # Make sure the city is updated
        city = storage.get(City, self.city.id)
        self.assertEqual(city.name, 'Los Angeles')


if __name__ == '__main__':
    unittest.main()
