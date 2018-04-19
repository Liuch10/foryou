from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, SelectField, SubmitField, FileField
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


class uploadCaseForm(Form):
    patient_name = StringField(validators=[Length(max=15)])
    patient_gender = SelectField(choices=[('0', '未知/保密'), ('1', '男'), ('2', '女')])
    patient_photo_type = SelectField(
        choices=[('0', '其他'), ('1', 'CR'), ('2', 'DR'), ('3', 'CT'), ('4', 'MR'), ('5', '超声')])
    patient_photo_file = StringField(validators=[Required()])
    submit = SubmitField('Upload')
