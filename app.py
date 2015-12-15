from flask import Flask , render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_set import Base, Team, Player

app = Flask(__name__)

engine = create_engine('sqlite:///teamroster.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/signIn/')
def signIn():
    return render_template('signIn.html')

@app.route('/signUp/')
def signUp():
    return render_template('signUp.html')

@app.route('/<int:team_id>/out/')
def teamOut(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    players = session.query(Player).filter_by(team_id = team_id).all()
    return render_template('teamOut.html', team=team, players=players)
	
@app.route('/<int:user_id>/profile/')
def profile(user_id):
    teams = session.query(Team).all()
    players = session.query(Player).all()
    return render_template('profile.html', teams=teams, players=players,user_id=user_id)

@app.route('/<int:user_id>/<int:team_id>/in/')
def teamIn(user_id, team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    players = session.query(Player).filter_by(team_id = team_id).all()
    return render_template('teamIn.html', team=team, players=players,user_id=user_id)

@app.route('/')
def homeScreen():
    teams = session.query(Team).all()
    team = session.query(Team).first()
    players = session.query(Player).all()
    return render_template('teams.html',teams=teams, players=players)


@app.route('/<int:user_id>/addTeam/', methods=['GET','POST'])
def addTeam(user_id):
    if request.method == 'POST':
        newTeam = Team(name = request.form['name'])
        session.add(newTeam)
        session.commit()
        return redirect(url_for('teamIn', user_id=user_id,team_id=newTeam.id))
    else:
        return render_template('addTeam.html',user_id=user_id)


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


@app.route('/<int:user_id>/<int:team_id>/newPlayer/', methods=['GET','POST'])
def addPlayer(user_id,team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    if request.method == 'POST':
        if request.form['name']:
            newPlayer = Player(name = request.form['name'], team_id = team.id)
            session.add(newPlayer)
            session.commit()
            return redirect(url_for('profile',user_id=user_id))
    else:
        return render_template('addPlayer.html',user_id=user_id,team_id=team.id,team=team)
        
    

@app.route('/<int:user_id>/<int:team_id>/editTeam/', methods=['GET','POST'])
def editTeam(user_id,team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    if request.method == 'POST':
        if request.form['name']:
            team.name = request.form['name']
        session.add(team)
        session.commit()
        return redirect(url_for('teamIn',user_id=user_id,team_id = team_id))
    else:
        return render_template('editTeam.html',user_id=user_id, team=team)

@app.route('/<int:user_id>/<int:team_id>/<int:player_id>/delete/',  methods=['GET','POST'])
def deletePlayer(user_id, team_id, player_id):
    team = session.query(Team).filter_by(id = team_id).one()
    itemToDelete = session.query(Player).filter_by(id=player_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('teamIn', user_id=user_id, team_id=team.id))
    else:
        return render_template('deletePlayer.html',user_id=user_id, itemToDelete=itemToDelete, team=team)

@app.route('/<int:user_id>/<int:team_id>/<int:player_id>/editPlayer', methods=['GET','POST'])
def editPlayer(user_id, team_id, player_id):
    player = session.query(Player).filter_by(id = player_id).one()
    team = session.query(Team).filter_by(id=team_id).one()
    if request.method == 'POST':
        if request.form['name']:
            player.name = request.form['name']
        session.add(player)
        session.commit()
        return redirect(url_for('teamIn',user_id=user_id, team_id = team.id))
    else:
        return render_template('editPlayer.html',user_id=user_id, team=team, player_id=player_id, player=player)
        
@app.route('/<int:user_id>/<int:team_id>/deleteTeam/', methods=['GET','POST'])
def deleteTeam(user_id, team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    if request.method == 'POST':
        session.delete(team)
        session.commit()
        return redirect(url_for('profile', user_id=user_id))
    else:
        return render_template('deleteTeam.html',user_id=user_id, team_id=team.id, team=team)

        

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
