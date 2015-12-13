from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_set import Team, Base, Player

engine = create_engine('sqlite:///teamroster2.db')
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
team1 = Team(name="TEAM1")

session.add(team1)
session.commit()

player1 = Player(name="Jamal", description="Jamal description",
                      team=team1)

session.add(player1)
session.commit()


player2 = Player(name="WIllis", description="WILSLDFSDFS",
                      team=team1)

session.add(player2)
session.commit()
player3 = Player(name="doucd", description="WILSLDFdsrrSDFS",
                      team=team1)

session.add(player3)
session.commit()


