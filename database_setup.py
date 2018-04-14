import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

@property
def serialize(self):
    """Return object data in easily serializable format"""
    return {
        'id'    :   self.id,
        'name'  :   self.name,
        'email' :   self.email,
        'picture'   :   self.picture,
    }

class Years(Base):

    __tablename__ = 'years'

    id = Column(Integer, primary_key = True)
    yearmonth = Column(String(255), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        return {
        'id'    :self.id,
        'yearmonth' :self.yearmonth,
        }

class Games(Base):

    __tablename__ = 'games'

    id = Column(Integer, primary_key = True)
    opponent = Column(String(255), nullable = False)
    description = Column(String(500))
    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship(Years)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
        'opponent'          :self.opponent,
        'description'   :self.description,
        'id'            :self.id,
        }

engine = create_engine('sqlite:///Wildcat.db')

Base.metadata.create_all(engine)
