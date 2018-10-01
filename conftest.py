import os
import random

import pytest

import models
import main

@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    models.init_db() 
    client = main.app.test_client()
    yield client