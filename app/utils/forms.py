from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, TextField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import Required, Length

class LoginForm(Form):
	username = StringField(validators = [Required(), Length(max = 15)])
	password = StringField(validators = [Required(), Length(max = 15)])
	submit = SubmitField('Login')

class SignUpForm(Form):
	username = StringField(validators = [Required(), Length(max = 15)])
	password = StringField(validators = [Required(), Length(max = 15)])
	submit = SubmitField('Sign up')
