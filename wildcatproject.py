from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   jsonify)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Years, Games, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Wildcat Seasons"


engine = create_engine('sqlite:///wildcat.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width:300px; height:300px;border-radius:150px;" \
                "-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/years/JSON')
def yearsJSON():
    years = session.query(Years).all()
    return jsonify(Years=[i.serialize for i in years])


@app.route('/years/<int:year_id>/JSON')
@app.route('/years/<int:year_id>/gms/JSON')
def yearGmsJSON(year_id):
    year = session.query(Years).filter_by(id=year_id).one()
    gms = session.query(Games).filter_by(year_id=year_id).all()
    return jsonify(Gms=[i.serialize for i in gms])


@app.route('/years/<int:year_id>/gms/<int:gms_id>/JSON/')
def GmsJSON(year_id, gms_id):
    gms = session.query(Games).filter_by(id=gms_id).one()
    return jsonify(Gms=gms.serialize)


@app.route('/')
@app.route('/years/')
def years():
    yearmonths = session.query(Years).order_by(asc(Years.yearmonth))
    if 'username' not in login_session:
        return render_template('publicyears.html', years=yearmonths)
    else:
        return render_template('years.html', yearmonths=yearmonths)


@app.route('/years/new', methods=['GET', 'POST'])
def newYear():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newYear = Years(yearmonth=request.form['yearmonth'],
                        user_id=login_session['user_id'])
        session.add(newYear)
        session.commit()
        flash("new Year created!")
        return redirect(url_for('years'))
    else:
        return render_template('newYear.html')


@app.route('/years/<int:year_id>/edit', methods=['GET', 'POST'])
def editYear(year_id):
    editedYear = session.query(Years).filter_by(id=year_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedYear.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
               "to edit this Year. Please create your own year in order to "\
               "edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['yearmonth']:
            editedYear.yearmonth = request.form['yearmonth']
        session.add(editedYear)
        session.commit()
        flash("Year has been edited")
        return redirect(url_for('years'))
    else:
        return render_template('editYear.html', year_id=year_id, i=editedYear)


@app.route('/years/<int:year_id>/delete', methods=['GET', 'POST'])
def deleteYear(year_id):
    deletedYear = session.query(Years).filter_by(id=year_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletedYear.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
               "to delete this year. Please create your own year in order to "\
               "delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedYear)
        session.commit()
        flash("Year has been deleted")
        return redirect(url_for('years'))
    else:
        return render_template('deleteYear.html', i=deletedYear)


@app.route('/years/<int:year_id>/')
@app.route('/years/<int:year_id>/gms')
def yearGms(year_id):
    year = session.query(Years).filter_by(id=year_id).one()
    creator = getUserInfo(year.user_id)
    games = session.query(Games).filter_by(year_id=year.id).all()
    if 'username' not in login_session or \
         creator.id != login_session['user_id']:
        return render_template('publicgms.html', year=year, creator=creator,
                                games=games)
    else:
        return render_template('gms.html', year=year, games=games)


@app.route('/years/<int:year_id>/new', methods=['GET', 'POST'])
def newGame(year_id):
    if 'username' not in login_session:
        return redirect('/login')
    year = session.query(Years).filter_by(id=year_id).one()
    if login_session['user_id'] != year.user_id:
        return "<script>function myFunction() {alert('You are not authorized "\
               "to add games to this year.  Please create your own year in "\
               "order to add games.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newGms = Games(opponent=request.form['opponent'],
                    description=request.form['description'],
                    year_id=year_id, user_id=login_session['user_id'])
        session.add(newGms)
        session.commit()
        flash("new game created!")
        return redirect(url_for('yearGms', year_id=year_id))
    else:
        return render_template('newGms.html', year_id=year_id)


@app.route('/years/<int:year_id>/<int:gms_id>/edit', methods=['GET', 'POST'])
def editGame(year_id, gms_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedGms = session.query(Games).filter_by(id=gms_id).one()
    year = session.query(Years).filter_by(id=year_id).one()
    yearList = session.query(Years).all()
    if login_session['user_id'] != year.user_id:
        return "<script>function myFunction() {alert('You are not authorized "\
               "to edit games in this year.  Please create your own year to "\
               "be able to edit games.');} " \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['opponent']:
            editedGms.name = request.form['opponent']
        if request.form['description']:
            editedGms.description = request.form['description']
        if request.form['yearlist']:
            editedGms.year_id = request.form['yearlist']
        session.add(editedGms)
        session.commit()
        flash("Game has been edited")
        return redirect(url_for('yearGms', year_id=year_id))
    else:
        return render_template('editGms.html', year_id=year_id, gms_id=gms_id,
                               i=editedGms, option_list=yearList)


@app.route('/years/<int:year_id>/<int:gms_id>/delete', methods=['GET', 'POST'])
def deleteGame(year_id, gms_id):
    if 'username' not in login_session:
        return redirect('/login')
    year = session.query(Years).filter_by(id=year_id).one()
    GmsToDelete = session.query(Games).filter_by(id=gms_id).one()
    if login_session['user_id'] != year.user_id:
        return "<script>function myFunction() {alert('You are not authorized' \
               'to delete a game in this year.  Please create your own year ' \
               'to delete games.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(GmsToDelete)
        session.commit()
        flash("Game has been deleted")
        return redirect(url_for('yearGms', year_id=year_id))
    else:
        return render_template('deleteGms.html', i=GmsToDelete)


@app.route('/years/<int:year_id>/<int:gms_id>/description')
def gmsDesc(year_id, gms_id):
    year = session.query(Years).filter_by(id=year_id).one()
    creator = getUserInfo(year.user_id)
    game = session.query(Games).filter_by(id=gms_id).one()
    if 'username' not in login_session or \
       creator.id != login_session['user_id']:
        return render_template('publicgmsDesc.html', year=year, game=game,
                               creator=creator)
    else:
        return render_template('gmsDesc.html', year=year, game=game,
                               creator=creator)


@app.route('/years/<int:year_id>/<int:gms_id>/cleardesc',
           methods=['GET', 'POST'])
def clearDesc(year_id, gms_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedGms = session.query(Games).filter_by(id=gms_id).one()
    yearList = session.query(Years).all()
    year = session.query(Years).filter_by(id=year_id).one()
    if login_session['user_id'] != year.user_id:
        return "<script>function myFunction() {alert('You are not authorized "\
               "to delete the description of this game. Please create your "\
               "own year and games and descriptions to be able to delete a "\
               "description');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
            editedGms.description = ""
            session.add(editedGms)
            session.commit()
            flash("Description has been deleted")
            return redirect(url_for('yearGms', year_id=year_id))
    else:
            return render_template('deleteDesc.html',
                                   year_id=year_id, gms_id=gms_id, i=editedGms)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
