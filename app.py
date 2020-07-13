"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, redirect, session, flash
from models import db, connect_db, User
from sqlalchemy import func
from forms import NewUserForm, LoginUserForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# CORS(app)

# from forms import AddCupcakeForm

# custom 404
@app.errorhandler(404)
def page_not_found(e):
  '''custom 404'''
  # note that we set the 404 status explicitly
  return render_template('404.html'), 404

@app.route('/')
def index():
  '''home page'''
  return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_new():
  '''display new user form(GET),register new user(POST)'''
  # display new user form
  form = NewUserForm()
  # if valid form post
  if form.validate_on_submit():
    un = form.username.data
    pwd = form.password.data
    eml = form.email.data
    fn = form.first_name.data
    ln = form.last_name.data
    # create new user
    user = User.register(un,pwd,eml,fn,ln)
    db.session.add(user)
    db.session.commit()
    # add new user to current session
    session['username'] = user.username
    print('user added: ', user)
    return redirect('/secret')
  # if get or not valid post
  else:
    return render_template('new_user.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_user():
  ''' show login form or login new user'''
  # login form
  form = LoginUserForm()
  # validate post
  if form.validate_on_submit():
    un = form.username.data
    pwd = form.password.data
    # authenticate user in User class
    user = User.authenticate(un,pwd)
    if user:
      session['username'] = user.username
      flash(f'logged in as {user.username}')
      return redirect('/secret')
    else:
      form.username.errors = ['Incorrect Username or Password']
  return render_template('/login.html',form=form)

@app.route('/logout')
def logout_user():
  session.pop('username')
  flash('you have logged out')
  return redirect('/login')

@app.route('/secret')
def secret_route():
  if 'username' not in session:
    flash('you must be logged in!')
    return redirect('/login')
  else:
    return render_template('/secret.html')