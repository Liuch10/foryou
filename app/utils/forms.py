from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, TextField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import Required, Length

class LoginForm(Form):
    user_name           = StringField(validators = [Required(), Length(max = 15)])
    user_password       = StringField(validators = [Required(), Length(max = 15)])
    submit = SubmitField('Login')

class SignUpForm(Form):
    user_name           = StringField(validators = [Required(), Length(max = 15)])
    user_password       = StringField(validators = [Required(), Length(max = 15)])
    user_type           = StringField(validators = [Required(), Length(max = 15)])
    user_city           = StringField(validators = [Required(), Length(max = 15)])
    user_hospital       = StringField(validators = [Required(), Length(max = 15)])
    user_department     = StringField(validators = [Required(), Length(max = 15)])
    user_phone          = StringField(validators = [Required(), Length(max = 15)])
    user_chain_address  = StringField(validators = [Required(), Length(max = 15)])
    submit = SubmitField('Sign up')
