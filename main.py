#!/usr/bin/env python3
'''
token acquisition/use service
'''
# standard python
import logging
import json

# third party libs
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import redirect

# our stuff
import utils
import models

APP = Flask(__name__)

# make a LOGGER
LOGGER = logging.getLogger("tokenservice")
LOGGER.setLevel(logging.INFO)

# create a FORMATTER
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# make some handlers
CONSOLE_HANDLER = logging.StreamHandler() # by default, sys.stderr
FILE_HANDLER = logging.FileHandler("logs.txt")
CONSOLE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)

# set logging levels
CONSOLE_HANDLER.setLevel(logging.WARNING)
CONSOLE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setLevel(logging.ERROR)

# add handlers to LOGGER
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.addHandler(FILE_HANDLER)

DBsession = sessionmaker(bind=models.engine)
session = DBsession()


API_KEY_LEN = 32

@APP.route("/get_token", methods=['GET'])
def get_api_get():
    '''
    Generate and return an token in json format after adding it to
    the database
    '''
    token_string = utils.get_random_number(length=API_KEY_LEN)
    token = models.Token(token=token_string)

    session.add(token)
    session.commit()

    return jsonify({"token": token_string})

@APP.route("/put", methods=['POST'])
def put():
    '''
    Handle a put to add data for a particular token
    '''
    token = json.loads(request.get_json())["token"]
    data = json.loads(request.get_json())["data"]

    LOGGER.info("Putting data {} for token {}".format(data, token))
    token = session.query(models.Token).filter(models.Token.token==token).one()
    LOGGER.debug("Got existing token {}".format(token))
    token.data = data

    session.commit()

    return jsonify({"did_insert": True})

@APP.route("/poll", methods=['POST'])
def poll():
    '''
    Handle a poll for data for a particular token
    '''
    token = json.loads(request.get_json())["token"]
    LOGGER.info("Got token {}".format(token))
    result = session.query(models.Token).filter(models.Token.token==token).one()
    return jsonify(result.data)

def start():
    APP.run()

def stop():
    pass

if __name__ == "__main__":
    start()
