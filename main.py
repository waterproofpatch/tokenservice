#!/usr/bin/env python3
'''
token acquisition/use service
'''
# standard python
import logging
import json
import string
import random
import base64

# third party libs
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import redirect
import sqlalchemy

# our stuff
import models

app = Flask(__name__)

# make a LOGGER
logging.basicConfig(format="%(asctime)s %(name)s %(filename)s:%(lineno)s - %(levelname)s - %(message)s",
                    level=logging.DEBUG)
LOGGER = logging.getLogger(name="tokenservice")


@app.route("/get_token", methods=['GET'])
def get_token():
    '''
    Generate and return an token in json format after adding it to
    the database
    '''
    token_string = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(32)])
    token = models.Token(token=token_string)

    models.get_db().add(token)
    models.get_db().commit()

    return jsonify({"token": token_string})


@app.route("/put", methods=['POST'])
def put():
    '''
    Handle a put to add data for a particular token
    '''
    token = request.get_json()["token"]
    data = request.get_json()["data"]

    try:
        existing_token = models.get_db().query(
            models.Token).filter(models.Token.token == token).one()
    except sqlalchemy.orm.exc.NoResultFound:
        return jsonify(), 400
    existing_token.data = base64.b64encode(data.encode())

    models.get_db().commit()

    return jsonify({"did_insert": True})


@app.route("/poll", methods=['POST'])
def poll():
    '''
    Handle a poll for data for a particular token
    '''
    token = request.get_json()["token"]
    try:
        result = models.get_db().query(models.Token).filter(
            models.Token.token == token).one()
    except sqlalchemy.orm.exc.NoResultFound:
        return jsonify(), 400

    if not result.data:
        return jsonify()
    return jsonify(base64.b64decode(result.data).decode())


if __name__ == "__main__":
    models.init_db()
    app.run()
