import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import app

Base = declarative_base()
engine = None
session = None

def init_db():
    global Base
    global engine
    # use an in-memory sqlite DB for test
    if app.config['TESTING']:
        engine = create_engine('sqlite://')
    else:
        engine = create_engine('sqlite:///prod.sqlite3')
    Base.metadata.create_all(engine)

def get_db():
    global session
    if not session:
        DBsession = sessionmaker(bind=engine)
        session = DBsession()
    return session

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    data = Column(LargeBinary)

    def __repr__(self):
        return '<Token(id={}, token={}, data={})>'.format(self.id, self.token, self.data)
