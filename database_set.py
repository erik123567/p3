import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)



class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Player(Base):
    __tablename__ = 'player'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship(Team)
	
# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'team_id': self.team_id,
        }


engine = create_engine('sqlite:///teamroster.db')


Base.metadata.create_all(engine)

