from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

post_keywords = Table('token_hostnames', Base.metadata,
     Column('token_id', ForeignKey('tokens.id'), primary_key=True),
     Column('hostname_id', ForeignKey('hostnames.id'), primary_key=True)
)

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    hostnames = relationship('Hostname', secondary=post_keywords, back_populates='tokens')

class Hostname(Base):
    __tablename__ = "hostnames"

    id = Column(Integer, primary_key=True)
    host = Column(String)
    domain = Column(String)
    tokens = relationship('Token', secondary=post_keywords, back_populates='hostnames')


def db(connectionstring, echo=True):
    engine = create_engine(connectionstring, echo=echo)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
