from flask_wtf import FlaskForm as Form
from flask import jsonify
from wtforms.fields import StringField, SelectField, SubmitField, PasswordField, RadioField, BooleanField
from wtforms.validators import Required, Length, NumberRange, ValidationError, Email, EqualTo

import json


class LoginForm(Form):
    user_mail = StringField(validators=[Required()])
    user_password = PasswordField(validators=[Required()])
    submit = SubmitField('Login')


def DoctorUser(form, field):
    if field.data != "doctor":
        raise ValidationError('目前只开放医生注册')


class SignUpForm(Form):
    user_mail = StringField(validators=[Email(message='请输入正确的邮箱格式')])
    # user_name = StringField(validators=[Length(max=15)])
    user_password = PasswordField(validators=[EqualTo('user_confirm_password', '两次输入密码一致')])
    user_confirm_password = PasswordField()

    # user_type = RadioField(choices=[('doctor', '医生'), ('patient', '普通用户（后续开放）')])
    user_type = RadioField(choices=[('doctor', '医生')])
    # user_type = StringField(validators=[Required(), Length(max=15)])
    user_city = SelectField(choices=[('北京', '北京'), ('江西', '江西'), ('内蒙古', '内蒙古'), ('云南', '云南'), ('其他', '其他')])
    user_hospital = StringField(validators=[Length(max=15)])
    user_department = StringField(validators=[Length(max=15)])
    # user_title = StringField(validators=[Length(max=15)])
    user_phone = StringField(validators=[Length(max=15)])
    # user_chain_address = StringField(validators=[])
    user_verification_code = StringField(validators=[Length(max=6)])
    submit = SubmitField('注册')


class CaseForm(Form):
    case_id = StringField()
    patient_name = StringField(validators=[Length(max=15)])
    patient_gender = SelectField(choices=[('未知', '未知/保密'), ('男', '男'), ('女', '女')])
    patient_age = StringField(validators=[NumberRange(min=0, max=100)])
    patient_photo_type = SelectField(
        choices=[('其他', '其他'), ('CR', 'CR'), ('DR', 'DR'), ('CT', 'CT'), ('MR', 'MR'), ('超声', '超声')])
    # patient_photo_file = StringField(validators=[Required()])
    case_photo_hash = StringField()
    is_diagnois = StringField()
    is_expert = StringField()
    patient_diagnois_type = SelectField(choices=[('良性', '良性'), ('恶性', '恶性')])
    patient_diagnois_result = SelectField(choices=[('0', '正常'), ('1', '一期'), ('2', '二期'), ('3', '三期')])
    doctor_name = StringField()
    doctor_hospital = StringField()
    doctor_department = StringField()
    case_upload_time = StringField()
    case_diagnois_time = StringField()
    case_expert_time = StringField()
    submit = SubmitField('发布')


class DiagnoseForm(Form):
    case_id = StringField(default="0")
    # case_patient_age = StringField(default="0")
    photo_quality = SelectField(choices=[('未选择', '未选择'),
                                         ('一级片', '一级片'),
                                         ('二级片', '二级片'),
                                         ('三级片', '三级片'),
                                         ('四级片', '四级片')])
    small_shadow_1 = StringField(default="")
    small_shadow_2 = StringField(default="")
    damage_1 = StringField(default="1/0")
    damage_2 = StringField(default="2/0")
    damage_3 = StringField(default="3/0")
    damage_4 = StringField(default="4/0")
    damage_5 = StringField(default="5/0")
    damage_6 = StringField(default="6/0")
    intensity = SelectField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], default="0")

    other_sign = StringField(default="无")

    bool_small_shadow = BooleanField('小阴影聚集', default=False)
    bool_big_shadow = BooleanField('大阴影', default=False)
    bool_pleural_plaque = BooleanField('胸膜斑', default=False)
    bool_big_shadow_2_1 = BooleanField('大阴影达到2*1', default=False)
    bool_pleural_calcification = BooleanField('胸膜钙化', default=False)
    bool_shadow_disorder = BooleanField('心影紊乱', default=False)

    level = SelectField(choices=[('无尘肺', '无尘肺'),
                                 ('一期', '一期'),
                                 ('二期', '二期'),
                                 ('三期', '三期')], default="无尘肺")
    remark = StringField(default="无")
    submit = SubmitField('提交标注')

    @staticmethod
    def build_form_from_json_string(data):
        print(data)
        d_json = json.loads(data)
        form = DiagnoseForm(case_id=int(d_json['case_id']),
                            # case_patient_age=d_json['case_patient_age'] ,
                            photo_quality=d_json['photo_quality'],
                            small_shadow_1=d_json['small_shadow_1'],
                            small_shadow_2=d_json['small_shadow_2'],
                            damage_1=d_json['damage_1'],
                            damage_2=d_json['damage_2'],
                            damage_3=d_json['damage_3'],
                            damage_4=d_json['damage_4'],
                            damage_5=d_json['damage_5'],
                            damage_6=d_json['damage_6'],
                            intensity=d_json['intensity'],
                            other_sign=d_json['other_sign'],

                            bool_small_shadow=True if 'bool_small_shadow' in d_json else False,
                            bool_big_shadow=True if 'bool_big_shadow' in d_json else False,
                            bool_pleural_plaque=True if 'bool_pleural_plaque' in d_json else False,
                            bool_big_shadow_2_1=True if 'bool_big_shadow_2_1' in d_json else False,
                            bool_pleural_calcification=True if 'bool_pleural_calcification' in d_json else False,
                            level=d_json['level'],
                            remark=d_json['remark'])

        return form
