from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_set import Base, Team, Player
engine = create_engine('sqlite:///teamroster.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
myFirstTeam = Team(name = "Bears")
session.add(myFirstTeam)
session.commit()
session.query(Team).all()
rice = Player(name = "Ray Rice", description = "Hi im race rice description", team = myFirstTeam)
session.add(rice)
session.commit()
session.query(Player).all()
firstResult = session.query(Player).first()
