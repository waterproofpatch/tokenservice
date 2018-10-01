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
    response = client.get('/get_token')
    assert response.status == '200 OK'
    assert json.loads(response.data.decode())['token'] is not None
    assert len(json.loads(response.data.decode())['token']) == 32

def test_get_unique_tokens(client):
    """
    Get two tokens and verify they are unique
    """
    response = client.get('/get_token')
    assert response.status == '200 OK'
    assert json.loads(response.data.decode())['token'] is not None
    assert len(json.loads(response.data.decode())['token']) == 32
    t1 = json.loads(response.data.decode())['token']

    response = client.get('/get_token')
    assert response.status == '200 OK'
    assert json.loads(response.data.decode())['token'] is not None
    assert len(json.loads(response.data.decode())['token']) == 32
    t2 = json.loads(response.data.decode())['token']

    assert t1 != t2