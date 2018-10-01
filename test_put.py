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
    response = client.get('/get_token')
    assert response.status == '200 OK'
    assert json.loads(response.data.decode())['token'] is not None
    assert len(json.loads(response.data.decode())['token']) == 64

    token = json.loads(response.data.decode())['token']

    response = client.post('/poll', json={"token": token})
    assert response.status == '200 OK'
    assert json.loads(response.data.decode()) == {}

    response = client.post('/put', json={"token": token, "data": "test data"})
    assert response.status == '200 OK'

    response = client.post('/poll', json={"token": token})
    assert response.status == '200 OK'
    assert json.loads(response.data.decode()) == 'test data'
