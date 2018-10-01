#!/usr/bin/env python3
import tempfile
import os
import json
import pytest

import main
import models


@pytest.fixture
def client():
    test_db_filename = 'test.sqlite3'
    try:
        os.remove(test_db_filename)
    except FileNotFoundError:
        pass
    os.environ['TEST_DB'] = test_db_filename
    models.init_db() 
    main.app.config['TESTING'] = True
    client = main.app.test_client()
    yield client

    # after client is done...
    try:
        os.remove(test_db_filename)
    except FileNotFoundError:
        pass


def test_get_new_token(client):
    """
    Get a new token
    """
    rv = client.get('/get_token')
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode())['token'] is not None
    assert len(json.loads(rv.data.decode())['token']) == 64
