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

@app.route('/<int:user_id>/add', methods=['GET','POST'])
def addTeam(user_id):
    if request.method == 'POST':
        newTeam = Team(name = request.form['name'])
        session.add(newTeam)
        session.commit()
        return redirect(url_for('showTeamsLoggedIn', user_id=user_id))
    else:
        return render_template('newTeam.html',user_id=user_id)


@app.route('/<int:user_id>/signedIn/')
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
        if request.form['name']:
            newPlayer = Player(name = request.form['name'], team_id = team.id)
            session.add(newPlayer)
            session.commit()
            return redirect(url_for('showRoster', team_id = team.id))
    else:
        return render_template('addPlayer.html', team_id=team.id,team=team)
        
    

@app.route('/<int:team_id>/editTeam/', methods=['GET','POST'])
def editTeam(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    if request.method == 'POST':
        if request.form['name']:
            team.name = request.form['name']
        session.add(team)
        session.commit()
        return redirect(url_for('showRoster',team_id = team_id))
    else:
        return render_template('editTeam.html', team=team)

@app.route('/<int:team_id>/<int:player_id>/delete')
def deletePlayer(team_id, player_id):
    team = session.query(Team).filter_by(id = team_id).one()
    player = session.query(Player).filter_by(id = player_id).one()
    return render_template('deletePlayer.html', team = team, player = player)


@app.route('/<int:team_id>/<int:player_id>/edit/', methods=['GET','POST'])
def editPlayer(team_id, player_id):
    player = session.query(Player).filter_by(id = player_id).one()
    team = session.query(Team).filter_by(id=team_id).one()
    if request.method == 'POST':
        if request.form['name']:
            player.name = request.form['name']
        session.add(player)
        session.commit()
        return redirect(url_for('showRoster',team_id = team_id))
    else:
        return render_template('editPlayer.html', team=team, player_id=player_id, player=player)
        
@app.route('/<int:team_id>/deleteTeam', methods=['GET','POST'])
def deleteTeam(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
        

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
