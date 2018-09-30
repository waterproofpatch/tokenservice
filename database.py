#!/usr/bin/env python3
'''
Database service
'''
import sqlite3
import base64
import logging

LOGGER = logging.getLogger("keeme")

def dict_factory(cursor, row):
    ''' 
    Handle a cursor and row result and turn into json
    '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database(object):
    '''
    Database class, encapsulates reading/writing data to/from database
    '''
    def __init__(self):
        '''
        Initialize the database
        '''
        LOGGER.info("Database starting...")
        self.conn = sqlite3.connect("db.db")
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS TOKENS (id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, token TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS DATA_STORE (id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, token TEXT, data TEXT)")
        self.conn.commit()

    def _submit_query(self, query):
        '''
        Internal query handler
        '''
        self.cur.execute(query)
        self.conn.commit()
        results = self.cur.fetchall()
        return results

    def _to_db_token(self, token):
        '''
        Return a database-safe token
        :param token: the token, in non-db safe form
        :return a database-safe token
        '''
        return base64.b64encode(token.encode()).decode()

    def put(self, token, data):
        '''
        Put some data in for an token
        '''
        # first check if the token is valid
        token = self._to_db_token(token=token)
        existing_tokens = self._submit_query("SELECT token FROM TOKENS WHERE token='{token}'".format(token=token))
        if len(existing_tokens) < 1:
            LOGGER.info("No tokens registered for {token}".format(token=token))
            return False
        self._submit_query("INSERT INTO DATA_STORE (token, data) VALUES ('{token}', '{data}')".format(token=token, data=data))
        return True

    def poll(self, token):
        '''
        Get any and all data ever 'put' for this token
        '''
        token = self._to_db_token(token=token)
        data = self._submit_query("SELECT data FROM DATA_STORE WHERE token='{token}'".format(token=token))
        LOGGER.info("Got data: {data}".format(data=data))
        return data

    def register_token(self, token):
        '''
        Register an token with the database
        '''
        token = base64.b64encode(token.encode()).decode()
        self._submit_query("INSERT INTO TOKENS (token) VALUES ('{token}')".format(token=token))
        
