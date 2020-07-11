from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def connect_db(app):
  '''connect to db'''
  db.app = app
  db.init_app(app)

class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String, nullable=False,unique=True)
  email = db.Column(db.EmailType(50), nullable=False,unique=True)
  first_name = db.Column(db.string(30), nullable=False)
  last_name = db.Column(db.string(30), nullable=False)

  @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"


  # def serialize(self):
  #   '''create a dictionary version of cupcake to convert to JSON'''
  #   return {
  #     'id': self.id,
  #     'flavor': self.flavor,
  #     'size': self.size,
  #     'rating': self.rating,
  #     'image': self.image
  #   }

  def __repr__(self):
	  return f'<User | {self.id} | {self.username} | {self.full_name}>'