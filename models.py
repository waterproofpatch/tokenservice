from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///tokens.sqlite3')

Base = declarative_base()


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    data = Column(String)

    def __repr__(self):
        return '<Token(id={}, token={}, data={})>'.format(self.id, self.token, self.data)

Base.metadata.create_all(engine)