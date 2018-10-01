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
    rv = client.get('/get_token')
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode())['token'] is not None
    assert len(json.loads(rv.data.decode())['token']) == 64

    # verify that there is nothing there for this token
    rv = client.post('/poll', json={"token": json.loads(rv.data.decode())["token"]})
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode()) == {}

def test_poll_invalid_token(client):
    """
    Verify we get a 400 for a poll on a token that does not exist
    """
    rv = client.post('/poll', json={"token": "doesnotexist"})
    assert rv.status == '400 BAD REQUEST'
    assert json.loads(rv.data.decode()) == {}