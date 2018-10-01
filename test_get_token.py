#!/usr/bin/env python3
import tempfile
import os
import json
import pytest

import main


@pytest.fixture
def client():
    db_fd, main.app.config['DATABASE'] = tempfile.mkstemp()
    main.app.config['TESTING'] = True
    client = main.app.test_client()

    # with main.app.app_context():
    #    main.init_db()

    yield client

    os.close(db_fd)
    os.unlink(main.app.config['DATABASE'])


def test_get_new_token(client):
    """
    Get a new token
    """
    rv = client.get('/get_token')
    assert rv.status == '200 OK'
    assert json.loads(rv.data.decode())['token'] is not None
    assert len(json.loads(rv.data.decode())['token']) == 64
