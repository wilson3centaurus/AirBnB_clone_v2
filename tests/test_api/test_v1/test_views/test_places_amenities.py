#!/usr/bin/python3
"""Unit tests for places_amenities module"""

import unittest
from flask import Flask
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


class TestPlacesAmenitiesAPI(unittest.TestCase):
    """
    Test cases for the endpoints managing the relationship
    between Place objects and Amenity objects.
    """

    def setUp(self):
        """Set up test client, Flask app, and initialize test data."""
        self.app = Flask(__name__)
        self.app.register_blueprint(app_views)
        self.client = self.app.test_client()
        self.place = Place(name="Mos Eisley Cantina",
                           description="A wretched hive of scum and villainy")
        self.amenity = Amenity(name="Wifi")
        storage.new(self.place)
        storage.new(self.amenity)
        storage.save()

    def tearDown(self):
        """Clean up after each test."""
        storage.delete(self.place)
        storage.delete(self.amenity)
        storage.save()

    def test_get_place_amenities(self):
        """
        Test GET /api/v1/places/<place_id>/amenities.
        """

        # Ensure GET request returns status code 200 and an empty list initially
        response = self.client.get(
            f'/api/v1/places/{self.place.id}/amenities'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 0)

        # Link an amenity to the place and ensure it's retrieved
        self.client.post(
            f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}'
        )
        response = self.client.get(
            f'/api/v1/places/{self.place.id}/amenities'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.amenity.id)

    def test_delete_place_amenity(self):
        """
        Test DELETE /api/v1/places/<place_id>/amenities/<amenity_id>.
        """

        # Link an amenity to the place
        self.client.post(
            f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}'
        )

        # Ensure DELETE request unlinks the amenity from the place
        response = self.client.delete(
            f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

        # Ensure the amenity is unlinked from the place
        response = self.client.get(
            f'/api/v1/places/{self.place.id}/amenities'
        )
        data = response.json
        self.assertEqual(len(data), 0)

    def test_link_place_amenity(self):
        """
        Test POST /api/v1/places/<place_id>/amenities/<amenity_id>.
        """

        # Ensure POST request links an amenity to the place
        response = self.client.post(
            f'/api/v1/places/{self.place.id}/amenities/{self.amenity.id}'
        )
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertEqual(data['id'], self.amenity.id)

        # Ensure the amenity is linked to the place
        response = self.client.get(
            f'/api/v1/places/{self.place.id}/amenities'
        )
        data = response.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.amenity.id)


if __name__ == '__main__':
    unittest.main()
