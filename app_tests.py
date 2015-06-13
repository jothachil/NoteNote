# -*- coding: utf-8 -*-
import app
import unittest

class FirstTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_index_response(self):
        rv = self.app.get('/')
        assert 'Enjoy coding!' in rv.data

if __name__ == "__main__":
    unittest.main()
