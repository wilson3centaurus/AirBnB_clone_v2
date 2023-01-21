#!/usr/bin/python3
"""
Contains tests for api v1 app
"""

import unittest

from api.v1.app import app


class TestApp(unittest.TestCase):
    """Test Class for Flask App
    """

    def setUp(self):
        """Sets up the flask app for testing"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Removes the flask app context"""
        self.ctx.pop()

    def test_app_status(self):
        """Test wether the status route returns 200"""
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)

    def test_app_json(self):
        """Test wether the status route returns 200"""
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.content_type, "application/json")
        self.assertIsNotNone(response.json["status"])
