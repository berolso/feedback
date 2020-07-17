"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, redirect, session, flash
from models import db, connect_db, User, Feedback
from sqlalchemy import func
from forms import NewUserForm, LoginUserForm, FeedbackForm
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
import inspect


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
  # show login if user is not
  if 'username' not in session:
    return redirect('/login')
  # if logged in show list of all comments
  feedback = Feedback.query.all()
  username = session['username']
  return render_template('index.html', feedback=feedback,username=username)

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
    # check for duplicate entry
    try:
      db.session.commit()
    except IntegrityError as e:
      # print(inspect.getmembers(e.orig.diag))
      # flash(e.orig.diag.message_detail,'danger')
      form.username.errors = [e.orig.diag.message_detail]
      return render_template('/new_user.html', form=form)
    # add new user to current session
    session['username'] = user.username
    flash('new user added','success')
    return redirect(f'/users/{user.username}')
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
      flash(f'logged in as {user.username}','success')
      return redirect(f'/users/{user.username}')
    else:
      form.username.errors = ['Incorrect Username or Password']
  return render_template('/login.html',form=form)

@app.route('/logout')
def logout_user():
  session.pop("username")
  flash('you have logged out','success')
  return redirect('/login')

@app.route('/users/<username>')
def user_route(username):
  '''show user page'''
  if 'username' not in session:
    # raise Unauthorized()
    flash('you must be logged in!','danger')
    return redirect('/login')
  else:
    user = User.query.filter_by(username=username).first()
    return render_template('/user.html',user=user)

@app.route('/users/<username>/delete')
def delete_user(username):
  '''delete user'''
  if "username" not in session or username != session['username']:
    # raise Unauthorized()
    flash('you must be logged in to delete user!','danger')
    return redirect(f'/login')
  user = User.query.filter_by(username=username).first()
  db.session.delete(user)
  db.session.commit()
  session.pop('username')
  return redirect('/login')
  
@app.route('/users/<username>/feedback/add',methods=["GET","POST"])
def new_feedback_form(username):
  '''create new feedback'''
  # verify user is logged in
  if "username" not in session or username != session['username']:
    flash('you must be logged in to add feedback user!','danger')
    return redirect(f'/login')
  # get user
  user = User.query.filter_by(username=username).first()

  form = FeedbackForm()
  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    # authenticate user in User class
    new_feedback = Feedback(title=title,content=content,username=username)
    if new_feedback:
      db.session.add(new_feedback)
      db.session.commit()
      flash(f'{username} added "{title}"','success')
      return redirect(f'/users/{username}')
    else:
      form.username.errors = ['Title must be less than 100 characters']
  return render_template('/feedback.html',form=form, user=user)

@app.route('/feedback/<int:id>/edit',methods=["GET","POST"])
def edit_feedback_form(id):
  '''edit feedback'''
  feedback = Feedback.query.get(id)
  # verify user is logged in
  if "username" not in session or feedback.username != session['username']:
    flash('you must be logged in to edit feedback!','danger')
    return redirect(f'/login')
  form = FeedbackForm(obj=feedback)
  if form.validate_on_submit():
    feedback.title = form.title.data
    feedback.content = form.content.data

    db.session.commit()

    return redirect(f"/users/{feedback.username}")

  return render_template("/feedback_edit.html", form=form, feedback=feedback)

@app.route('/feedback/<int:id>/delete',methods=["POST"])
def delete_feedback(id):
  '''delete feedback'''
  feedback = Feedback.query.get(id)
  # verify user is logged in
  if "username" not in session or feedback.username != session['username']:
    flash('you must be logged in to edit feedback!','danger')
    return redirect(f'/login')
  if form.validate_on_submit():

    db.session.delete(feedback)
    db.session.commit()

  return redirect(f"/users/{feedback.username}")
