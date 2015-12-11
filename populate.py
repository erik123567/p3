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

player2 = Player(name="Jamal", description="Jamal description",
                      team=team1)

session.add(player2)
session.commit()


player2 = Player(name="WIllis", description="WILSLDFSDFS",
                      team=team1)

session.add(player2)
session.commit()


# Roster for Falcons
team2 = Team(name="Falcons")

session.add(team2)
session.commit()

player2 = Player(name="Tina", description="Tina descp",
                      team=team2)

session.add(player2)
session.commit()


player2 = Player(name="Linda", description="Linda description",
                      team=team2)

session.add(player2)
session.commit()

# Roster for Pandas
team3 = Team(name="Pandas")

session.add(team3)
session.commit()

player2 = Player(name="Pdadr", description="yusdr ",
                      team=team3)

session.add(player2)
session.commit()


player2 = Player(name="differ", 	description="beep description",
                      team=team3)

session.add(player2)
session.commit()



