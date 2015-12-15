from flask import Flask , render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_set import Base, Team, Player

app = Flask(__name__)

engine = create_engine('sqlite:///teamroster.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def showTeams():
    teams = session.query(Team).all()
    team = session.query(Team).first()
    players = session.query(Player).all()
    return render_template('showRosters.html',teams=teams, players=players)

@app.route('/<user_id>/add', methods=['GET','POST'])
def addTeam(user_id):
    if request.method == 'POST':
        newTeam = Team(name = request.form['name'])
        session.add(newTeam)
        session.commit()
    return render_template('newTeam.html',user_id=user_id)

@app.route('/<user_id>/signedIn/')
def showTeamsLoggedIn(user_id):
    teams = session.query(Team).all()
    team = session.query(Team).first()
    players = session.query(Player).all()
    return render_template('showRosterLoggedIn.html',teams=teams, players=players,user_id=user_id)
	
	
@app.route('/roster/<int:team_id>/')
def showRoster(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    players = session.query(Player).filter_by(team_id=team_id)
    return render_template('showTeam.html', team = team, players = players)


@app.route('/<int:team_id>/new', methods=['GET','POST'])
@app.route('/roster/<int:team_id>/new/', methods=['GET','POST'])
def addPlayer(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    if request.method == 'POST':
        newPlayer = Player(name = request.form['name'], team_id = team.id)
        session.add(newPlayer)
        session.commit()
        return redirect(url_for('showRoster', team_id = team.id))
    else:
        return render_template('addplayer.html', team_id=team.id)
        
    

@app.route('/<int:team_id>/editTeam/')
def editTeam(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    return "page to edit %s" % team.name

@app.route('/<int:team_id>/<int:player_id>/delete')
def deletePlayer(team_id, player_id):
    team = session.query(Team).filter_by(id = team_id).one()
    player = session.query(Player).filter_by(id = player_id).one()
    return render_template('deletePlayer.html', team = team, player = player)


@app.route('/<int:team_id>/<int:player_id>/edit/')
def editPlayer(team_id, player_id):
    player = session.query(Player).filter_by(id = player_id).one()
    return "page to edit %s" % player.name

@app.route('/<int:team_id>/deleteTeam')
def deleteTeam(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    return render_template('deleteTeam.html', team = team)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
