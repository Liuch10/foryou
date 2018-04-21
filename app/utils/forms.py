from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, SelectField, SubmitField, PasswordField, RadioField
from wtforms.validators import Required, Length, NumberRange, ValidationError, Email, EqualTo


class LoginForm(Form):
    user_mail = StringField(validators=[Required(), Length(max=15)])
    user_password = PasswordField(validators=[Required()])
    submit = SubmitField('Login')


def DoctorUser(form, field):
    if len(field.data) != "doctor":
        raise ValidationError('目前只开放医生注册')


class SignUpForm(Form):
    user_mail = StringField(validators=[Required(), Email(message='请输入正确的邮箱格式')])
    user_name = StringField(validators=[Required(), Length(max=15)])
    user_password = PasswordField(validators=[Required(), EqualTo('user_confirm_password', '两次输入密码一致')])
    user_confirm_password = PasswordField(validators=[Required()])

    user_type = RadioField(choices=[('doctor', '医生'), ('patient', '普通用户（后续开放）')], validators=[DoctorUser])
    # user_type = StringField(validators=[Required(), Length(max=15)])
    user_city = SelectField(choices=[('北京', '北京'), ('江西', '江西'), ('内蒙古', '内蒙古'), ('云南', '云南'), ('其他', '其他')])
    user_hospital = StringField(validators=[Required(), Length(max=15)])
    user_department = StringField(validators=[Required(), Length(max=15)])
    user_title = StringField(validators=[Required(), Length(max=15)])
    user_phone = StringField(validators=[Required(), Length(max=15)])
    user_chain_address = StringField(validators=[Required(), Length(max=15)])
    user_verification_code = StringField(validators=[Required(), Length(max=6)])
    submit = SubmitField('注册')


class CaseForm(Form):
    case_id = StringField()
    patient_name = StringField(validators=[Length(max=15)])
    patient_gender = SelectField(choices=[('0', '未知/保密'), ('1', '男'), ('2', '女')])
    patient_age = StringField(validators=[NumberRange(min=0, max=100)])
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
    submit = SubmitField('发布')
