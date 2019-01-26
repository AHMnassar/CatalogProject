from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from DB_setup import Base, Year, CatalogItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, jsonify, url_for, flash
import requests


app = Flask(__name__)

# Google client_id
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Movies Catalog Application"

# Connect to database
engine = create_engine('postgresql://catalog:catalogpassword@localhost/catalog')
Base.metadata.bind = engine


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
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
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
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
    output += ' " style = "width: 300px; height: 300px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


@app.route('/gdisconnect')
def gdisconnect():
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
        response = redirect(url_for('showYears'))
        flash("You are now logged out.")
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON API's to view information
@app.route('/years/<int:year_id>/catalog/JSON')
def yearCatalogJSON(year_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    year = session.query(Year).filter_by(id=year_id).one()
    items = session.query(CatalogItem).filter_by(
        year_id=year_id).all()
    return jsonify(YearItems=[i.serialize for i in items])


@app.route('/years/<int:year_id>/catalog/<int:catalog_id>/JSON')
def catalogItemJSON(year_id, catalog_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catalogItem = session.query(CatalogItem).filter_by(id=catalog_id).one()
    return jsonify(CatalogItem=catalogItem.serialize)


@app.route('/years/JSON')
def yearsJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    years = session.query(Year).all()
    return jsonify(years=[r.serialize for r in years])


# Show all years
@app.route('/')
@app.route('/years/')
def showYears():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    years = session.query(Year).all()
    return render_template('Years.html', years=years)

# Create new year


@app.route('/years/new/', methods=['GET', 'POST'])
def newYear():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newYear = Year(name=request.form['name'],
                                   user_id=login_session['user_id'])
        session.add(newYear)
        session.commit()
        return redirect(url_for('showYears'))
    else:
        return render_template('newYear.html')

# Edit year


@app.route('/years/<int:year_id>/edit/', methods=['GET', 'POST'])
def editYear(year_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedYear = session.query(
        Year).filter_by(id=year_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedYear.user_id != login_session['user_id']:
        return "<script>{alert('Unauthorized');}</script>"
    if request.method == 'POST':
        if request.form['name']:
            editedYear.name = request.form['name']
            flash('Year Successfully Edited %s' % editedYear.name)
            session.add(editedYear)
            session.commit()
            return redirect(url_for('showYears'))
    else:
        return render_template('editYear.html',
                               year=editedYear)

# Delete year


@app.route('/years/<int:year_id>/delete/', methods=['GET', 'POST'])
def deleteYear(year_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    yearToDelete = session.query(
        Year).filter_by(id=year_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if yearToDelete.user_id != login_session['user_id']:
        return "<script>{alert('Unauthorized');}</script>"
    if request.method == 'POST':
        session.delete(yearToDelete)
        flash('%s Successfully Deleted' % yearToDelete.name)
        session.commit()
        return redirect(url_for('showYears'))
    else:
        return render_template('deleteYear.html',
                               year=yearToDelete)

# Show year catalog


@app.route('/years/<int:year_id>/')
@app.route('/years/<int:year_id>/catalog/')
def yearCatalog(year_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    year = session.query(Year).filter_by(id=year_id).one()
    items = session.query(
        CatalogItem).filter_by(year_id=year_id).all()
    return render_template('catalog.html', year=year, items=items)

# Create new catalog item


@app.route(
    '/years/<int:year_id>/catalog/new/', methods=['GET', 'POST'])
def newCatalogItem(year_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'],
                           description=request.form['description'],
                           theme=request.form['theme'],
                           year_id=year_id)
        session.add(newItem)
        session.commit()
        flash("Catalog Item has been added")
        return redirect(url_for('yearCatalog', year_id=year_id))
    else:
        return render_template('newcatalogitem.html', year_id=year_id)
    return render_template('newcatalogitem.html', year=year)

# Edit catalog item


@app.route('/years/<int:year_id>/<int:catalog_id>/edit/',
           methods=['GET', 'POST'])
def editCatalogItem(year_id, catalog_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CatalogItem).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['theme']:
            editedItem.theme = request.form['theme']
        session.add(editedItem)
        session.commit()
        flash("Catalog Item has been edited")

        return redirect(url_for('yearCatalog', year_id=year_id))
    else:
        return render_template(
            'editcatalogitem.html', year_id=year_id,
            catalog_id=catalog_id, item=editedItem)

# Delete catalog item


@app.route('/years/<int:year_id>/<int:catalog_id>/delete/',
           methods=['GET', 'POST'])
def deleteCatalogItem(year_id, catalog_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(CatalogItem).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Catalog has been deleted")
        return redirect(url_for('yearCatalog', year_id=year_id))
    else:
        return render_template('deletecatalogitem.html', item=itemToDelete)

# end of file
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=2200)
