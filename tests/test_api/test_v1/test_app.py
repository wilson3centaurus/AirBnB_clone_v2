#!/usr/bin/python3
"""Unit tests for app module"""

import inspect
import pep8
import unittest
import os
from api.v1 import app as app_module
from api.v1.app import app


class TestApp(unittest.TestCase):
    """Tests app module"""

    def setUp(self):
        """Set up Flask app for testing"""

        self.app = app.test_client()

    def test_cors_configuration(self):
        """Tests CORS configuration"""

        response = self.app.get('/')
        self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '0.0.0.0')

    def test_blueprint_registration(self):
        """Tests blueprint registration"""

        self.assertIn('app_views', app.blueprints)

    def test_error_handling(self):
        """Tests error handling"""

        response = self.app.get('/invalid_route')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Not found"})

    def test_environment_variables(self):
        """Tests environment variables"""

        app.config['HOST'] = os.environ.get('HBNB_API_HOST', '0.0.0.0')
        app.config['PORT'] = int(os.environ.get('HBNB_API_PORT', 5000))

        self.assertEqual(app.config['HOST'], '0.0.0.0')
        self.assertEqual(app.config['PORT'], 5000)

    def test_doc(self):
        """Tests module docstring existence"""

        self.assertIsNotNone(app_module.__doc__)

    def test_function_doc(self):
        """Tests function docstring existence (for all functions)"""

        functions = inspect.getmembers(app_module, inspect.isfunction)
        for function in functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8(self):
        """Tests if module follows PEP8 style"""

        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['api/v1/app.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_executable(self):
        """Tests if the file is executable"""

        file_stat = os.stat('api/v1/app.py')
        permissions = str(oct(file_stat[0]))
        expected = int(permissions[5:-2]) >= 5
        self.assertTrue(expected)


if __name__ == "__main__":
    unittest.main()
