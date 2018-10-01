#!/usr/bin/env python3
import tempfile
import os
import json
import pytest

import main
import models


def test_poll_valid_token(client):
    """
    Verify we get a valid response with no data for a token that does exist
    """
    response = client.get('/get_token')
    assert response.status == '200 OK'
    assert json.loads(response.data.decode())['token'] is not None
    assert len(json.loads(response.data.decode())['token']) == 32

    # verify that there is nothing there for this token
    response = client.post('/poll', json={"token": json.loads(response.data.decode())["token"]})
    assert response.status == '200 OK'
    assert json.loads(response.data.decode()) == {}

def test_poll_invalid_token(client):
    """
    Verify we get a 400 for a poll on a token that does not exist
    """
    rv = client.post('/poll', json={"token": "doesnotexist"})
    assert rv.status == '400 BAD REQUEST'
    assert json.loads(rv.data.decode()) == {}