import os

import pytest

import models
import main

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
