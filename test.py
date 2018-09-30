#!/usr/bin/env python3

import unittest
import json
from main import APP
import main as main

class TestTokenService(unittest.TestCase):

    def setUp(self):
        self.app = APP.test_client()
        self.app.testing=True

    def tearDown(self):
        pass

    def test_get(self):
        result = self.app.get('get_token')

        data = result.data.decode().strip()
        token = json.loads(data)["token"]

        self.assertEqual(len(token), main.API_KEY_LEN * 2)

    def test_put(self):
        result = self.app.get('get_token')

        data = result.data.decode().strip()
        token = json.loads(data)["token"]

        self.assertEqual(len(token), main.API_KEY_LEN * 2)

        # put something to this token and expect a 200 response
        data = json.dumps({"token":token, "data":"test data 123"})
        #data = {"token":token, "data":"test data 123"}
        print("Sending data {data}".format(data=data))
        res = self.app.post('put', content_type="application/json", data=data)
        print("RES: {}".format(res))

    def test_poll(self):
        pass

if __name__ == '__main__':
    unittest.main()
