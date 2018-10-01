import os

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = None
session = None

def init_db():
    global Base
    global engine
    db_file = os.environ.get('TEST_DB', 'prod.sqlite3')
    engine = create_engine('sqlite:///{}'.format(db_file))
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
