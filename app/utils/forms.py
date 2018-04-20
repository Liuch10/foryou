from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, SelectField, SubmitField
from wtforms.validators import Required, Length, NumberRange

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
    user_title          = StringField(validators = [Required(), Length(max = 15)])
    user_phone          = StringField(validators = [Required(), Length(max = 15)])
    user_chain_address  = StringField(validators = [Required(), Length(max = 15)])
    submit = SubmitField('Sign up')


class CaseForm(Form):
    case_id = StringField()
    patient_name = StringField(validators=[Length(max=15)])
    patient_gender = SelectField(choices=[('0', '未知/保密'), ('1', '男'), ('2', '女')])
    patient_age = StringField(validators=NumberRange(min=0, max=100))
    patient_photo_type = SelectField(
        choices=[('0', '其他'), ('1', 'CR'), ('2', 'DR'), ('3', 'CT'), ('4', 'MR'), ('5', '超声')])
    patient_photo_file = StringField(validators=[Required()])
    is_diagnois = StringField()
    is_expert = StringField()
    patient_diagnois_type = SelectField(choices=[('0', '良性'), ('1', '恶性')])
    patient_diagnois_result = SelectField(choices=[('0', '正常'), ('1', '一期'), ('2', '二期'), ('3', '三期')])
    doctor_name = StringField()
    doctor_hospital = StringField()
    doctor_department = StringField()
    case_upload_time = StringField()
    case_diagnois_time = StringField()
    case_expert_time = StringField()
    submit = SubmitField('Upload')
