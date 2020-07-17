from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, TextField
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, Optional,URL,NumberRange,Length


class NewUserForm(FlaskForm):
    """Form for registering new users."""

    username = StringField("UserName", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class LoginUserForm(FlaskForm):
    """Form for login users."""

    username = StringField("UserName", validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    '''Form for creating feedback'''
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = TextField('Content', validators=[InputRequired()])
    
