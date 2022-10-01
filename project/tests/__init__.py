import os
from flask_testing import TestCase
from init_db import init_test_data
from app import app
from unittest import TestCase as UnitTestCase
class BaseTestCase(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        if os.path.exists('test.db'):
            os.remove('test.db')
        os.environ['mode']='test'
        init_test_data()

    def tearDown(self):
        del os.environ['mode']

class BaseUnitTestCase(UnitTestCase):

    def setUp(self):
        if os.path.exists('test.db'):
            os.remove('test.db')
        os.environ['mode']='test'
        init_test_data()

    def tearDown(self):
        del os.environ['mode']