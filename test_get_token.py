#!/usr/bin/env python3
import tempfile
import os
import json
import pytest

import main
import models


def test_get_new_token(client):
    """
    Get a new token
    """
    rv = client.get('/get_token')
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode())['token'] is not None
    assert len(json.loads(rv.data.decode())['token']) == 64

def test_get_unique_tokens(client):
    """
    Get two tokens and verify they are unique
    """
    rv = client.get('/get_token')
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode())['token'] is not None
    assert len(json.loads(rv.data.decode())['token']) == 64
    t1 = json.loads(rv.data.decode())['token']

    rv = client.get('/get_token')
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode())['token'] is not None
    assert len(json.loads(rv.data.decode())['token']) == 64
    t2 = json.loads(rv.data.decode())['token']

    assert t1 != t2