from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_set import Base, Team, Player

app = Flask(__name__)

engine = create_engine('sqlite:///teamroster2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def showTeams():
    team = session.query(Team).all()

    output = ''
    for i in team:
        players = session.query(Player).filter_by(team_id=i.id)
        output += i.name + ' ROSTER' + '%s' % i.id
        output += '</br>'
        for p in players:
            output += '%s' % p.name
            output += '%s' % p.id
            output += '</br>'
        output += '</br>'
        

    return output
	

@app.route('/roster/<int:team_id>/')
def showRoster(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    players = session.query(Player).filter_by(team_id=team_id)
    output = '%s' % team.name + '</br>'
    for p in players:
        output += '%s' % p.name
        output += '%s' % p.id
        output += '</br>'
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)