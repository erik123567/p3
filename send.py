from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_set import Base, Team, Player
engine = create_engine('sqlite:///teamroster2.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
myFirstTeam = Team(name = "Bears")
session.add(myFirstTeam)
session.commit()
session.query(Team).all()
rice = Player(name = "Ray Rice", description = "BEFORE", team = myFirstTeam)
session.add(rice)
session.commit()
session.query(Player).all()

# DELETED player = session.query(Player).filter_by(name = "Ray Rice", id = 3 ).one()
falc = "Falcons"
team = session.query(Team).filter_by(name = falc)'
print team.id
#player = session.query(Player).filter_by(team_id=team.id)
#session.add(player)
print player.name
print player.id
print player.description

player.description = "updated"
session.add(player)
session.commit()

#riceDel = session.query(Player).filter_by(name = "Ray Rice", id = 3 ).one()
print riceDel.team_id
session.delete(riceDel)
session.commit()
#riceDel = session.query(Player).filter_by(name = "Ray Rice", id = 3 ).one()
print player.name
print player.id
print player.description


