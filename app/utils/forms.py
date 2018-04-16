from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, TextField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
    user_name = StringField(validators=[Required(), Length(max=15)])
    user_password = StringField(validators=[Required(), Length(max=15)])
    submit = SubmitField('Login')


class SignUpForm(Form):
    user_name = StringField(validators=[Required(), Length(max=15)])
    user_mail = StringField(validators=[Required(),Email()])
    user_password = StringField(validators=[Required(), Length(max=15)])
    user_type = StringField(validators=[Length(max=15)])
    user_city = StringField(validators=[Length(max=15)])
    user_hospital = StringField(validators=[Length(max=15)])
    user_department = StringField(validators=[Length(max=15)])
    user_phone = StringField(validators=[Length(max=15)])
    user_chain_address = StringField(validators=[Length(max=15)])
    user_verification_code = StringField(validators=[Required(), Length(max=6)])
    submit = SubmitField('Sign up')
