#!/usr/bin/env python3
import tempfile
import os
import json
import base64

import pytest

import main
import models


def test_put_valid_token(client):
    """
    Verify we get a token and add data to it and can get it back
    """
    rv = client.get('/get_token')
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode())['token'] is not None
    assert len(json.loads(rv.data.decode())['token']) == 64

    token = json.loads(rv.data.decode())['token']

    rv = client.post('/poll', json={"token": token})
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode()) == {}

    rv = client.post('/put', json={"token": token, "data": "test data"})
    assert rv.status == '200 OK'

    rv = client.post('/poll', json={"token": token})
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode()) == 'test data'
