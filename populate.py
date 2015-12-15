from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_set import Team, Base, Player

engine = create_engine('sqlite:///teamroster.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Roster for Bears
team1 = Team(name="Bears")

session.add(team1)
session.commit()
player1 = Player(name="Jamal", description="Jamal from florida",
                      team=team1)
session.add(player1)
session.commit()


player2 = Player(name="WIllis", description="willis from wiliyville",
                      team=team1)

session.add(player2)
session.commit()
player3 = Player(name="corey", description="corey from atlanta",
                      team=team1)

session.add(player3)
session.commit()

# ROSTER FOR LION

team2 = Team(name="Lions")
session.add(team2)
session.commit()
player1 = Player(name="Too", description="too decriptsd ",
                      team=team2)
session.add(player1)
session.commit()

player2 = Player(name="josh", description="la toole",
                      team=team2)
session.add(player2)
session.commit()
player3 = Player(name="barnad", description="fbradrr brandrr ",
                      team=team2)
session.add(player3)
session.commit()

# ROSTER FOR GIants

team3 = Team(name="Giants")
session.add(team3)
session.commit()
player1 = Player(name="peter", description="emptyd ",
                      team=team3)
session.add(player1)
session.commit()

player2 = Player(name="mumbo", description="munbo eat",
                      team=team3)
session.add(player2)
session.commit()
player3 = Player(name="lourl", description="lauren desc ",
                      team=team3)
session.add(player3)
session.commit()

