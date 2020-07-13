from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, Optional,URL,NumberRange


class NewUserForm(FlaskForm):
    """Form for registering new users."""

    username = StringField("UserName", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginUserForm(FlaskForm):
    """Form for login users."""

    username = StringField("UserName", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
