from flask import Flask , render_template, request, redirect, url_for, flash, jsonify, abort, request 
from uuid import uuid4
import requests
import requests.auth
import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_set import Base, Team, Player, User

CLIENT_ID = "xd7j_gpSVjjFOg"
CLIENT_SECRET = "UcLK8ARPNhvPCdDNtamQf5qPPCw"
REDIRECT_URI ="http://localhost:5000/reddit_callback"



def user_agent():
    '''reddit API clients should each have their own, unique user-agent
    Ideally, with contact info included.
    
    e.g.,
    return "oauth2-sample-app by /u/%s" % your_reddit_username
    '''
    return "oauth2-sample-app"
    #raise NotImplementedError()

def base_headers():
    return {"User-Agent": user_agent()}

app = Flask(__name__)

engine = create_engine('sqlite:///teamroster.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/<int:player_id>/showPlayerOut/')
def showPlayerOut(player_id):
    player = session.query(Player).filter_by(id = player_id).one()
    return render_template('showPlayerOut.html',player_id = player.id,player=player)

@app.route('/<int:user_id>/<int:player_id>/showPlayerIn/')
def showPlayerIn(user_id, player_id):
    player = session.query(Player).filter_by(id = player_id).one()
    return render_template('showPlayerIn.html', user_id = user_id, player_id = player.id, player = player)

@app.route('/signIn/')
def signIn():
    text = '<a href="%s">Authenticate with reddit</a>'
    return text % make_authorization_url()

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"}
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
    return url

def save_created_state(state):
    pass
def is_valid_state(state):
    return True

@app.route('/reddit_callback', methods=['GET','POST'])
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    username = get_username(access_token)
	
	

    newUser = User(username = username)
    # if the user is not there add and commit it
    #user = session.query(User).filter_by(username = newUser.username).first()
    #if user == None
       # session.add(newUser)
        # session.commit()
    #return 'this %s was added' % newUser.username
    #return 'this is %s ' % newUser.username
	# I NEED TO QUERY IN ORDER TO GET THIS USER FOR THE REDIRECT FOR THE ID YOU FUCKER
    session.add(newUser)
    session.commit()
	
    return render_template('userWelcome.html', user_id = newUser.id, username = newUser.username)
	
    #return redirect(url_for('profile.html',user_id = newUser.id, username = username))
	# REDIRECT TO A PLACE WITH THE USER NAME YOU NOW HAVE 
	# redireect to homescreen with hello USER 
    #return "Your reddit username is: %s" % get_username(access_token)

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]
    
    
def get_username(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']

@app.route('/signUp/')
def signUp():
    return render_template('signUp.html')

@app.route('/<int:team_id>/out/')
def teamOut(team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    players = session.query(Player).filter_by(team_id = team_id).all()
    return render_template('teamOut.html', team=team, players=players)

@app.route('/<int:user_id>/<int:team_id>/in/')
def teamIn(user_id, team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    players = session.query(Player).filter_by(team_id = team_id).all()
    return render_template('teamIn.html', team=team, players=players,user_id=user_id)
	
@app.route('/<int:user_id>/profile/', methods=['GET','POST'])
def profile(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    teams = session.query(Team).all()
    players = session.query(Player).all()
    return 'This is my username : %s' % user.username
    #return render_template('profile.html', teams=teams, players=players,user_id=user.id)
	
@app.route('/<int:user_id>/welcome/', methods=['GET','POST'])
def userWelcome(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    teams = session.query(Team).all()
    players = session.query(Player).all()
    return render_template('userWelcome.html',user_id=user.id,username = user.username)



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
        flash("new team created")
        return redirect(url_for('profile', user_id=user_id))
    else:
        return render_template('addTeam.html',user_id=user_id)




@app.route('/<int:user_id>/<int:team_id>/newPlayer/', methods=['GET','POST'])
def addPlayer(user_id,team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    if request.method == 'POST':
        if request.form['name']:
            newPlayer = Player(name = request.form['name'], team_id = team.id, description = request.form['description'])
            session.add(newPlayer)
            session.commit()
            flash("new player created!")
            return redirect(url_for('teamIn',user_id=user_id, team_id = team_id))
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
        flash("team edited ")
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
        flash("player deleted")
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
        if request.form['description']:
            player.description = request.form['description']
        session.add(player)
        session.commit()
        flash("player edited ")
        return redirect(url_for('teamIn',user_id=user_id, team_id = team.id))
    else:
        return render_template('editPlayer.html',user_id=user_id, team=team, player_id=player_id, player=player)
        
@app.route('/<int:user_id>/<int:team_id>/deleteTeam/', methods=['GET','POST'])
def deleteTeam(user_id, team_id):
    team = session.query(Team).filter_by(id = team_id).one()
    if request.method == 'POST':
        session.delete(team)
        session.commit()
        flash("team deleted")
        return redirect(url_for('profile', user_id=user_id))
    else:
        return render_template('deleteTeam.html',user_id=user_id, team_id=team.id, team=team)

#Making API Endpoint with a GET request
@app.route('/teams/<int:team_id>/JSON')
def teamJSON(team_id):
    team = session.query(Team).filter_by(id=team_id).one()
    players = session.query(Player).filter_by(
        team_id = team_id).all()
    return jsonify(Players=[i.serialize for i in players])    

        

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
