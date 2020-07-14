from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
  '''connect to db'''
  db.app = app
  db.init_app(app)

class User(db.Model):
  '''user class'''
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String, nullable=False,unique=True)
  password = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False,unique=True)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)

  @property
  def full_name(self):
    """Return full name of user."""
    return f"{self.first_name} {self.last_name}"

  @classmethod
  def register(cls, username, pwd, email, first_name, last_name):
    """Register user w/hashed password & return user."""

    hashed = bcrypt.generate_password_hash(pwd)
    # turn bytestring into normal (unicode utf8) string
    hashed_utf8 = hashed.decode("utf8")

    # return instance of user w/username and hashed pwd
    user = cls(username=username, password=hashed_utf8,email=email,first_name=first_name,last_name=last_name)

    return user

  @classmethod
  def authenticate(cls, username, pwd):
    """Validate that user exists & password is correct.

    Return user if valid; else return False.
    """

    u = User.query.filter_by(username=username).first()

    if u and bcrypt.check_password_hash(u.password, pwd):
        # return user instance
        return u
    else:
        return False

  def __repr__(self):
	  return f'<User | {self.id} | {self.username} | {self.full_name}>'