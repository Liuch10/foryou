from flask import Response, render_template, jsonify, request
from app.models.models import User, Case
from app.utils.forms import CaseForm
from app import db
from random import choice
from flask_login import current_user, login_required

# @login_required
def work():
    form = CaseForm()
    return render_template('work.html', form = form)

def work_start_comment():
    comment = request.form.get('comment')
    # TODO... update db
    return jsonify({'result':'success'})

def work_start_consult():
    comment = request.form.get('comment')
    # TODO... update db
    return jsonify({'result':'success'})

def work_update_expert():
    comment = request.form.get('comment')
    # TODO... update db
    return jsonify({'result':'success'})

def work_upload_case():
    case = Case()
    patient_name            = request.form.get('patient_name')
    patient_gender          = request.form.get('patient_gender')
    patient_age             = request.form.get('patient_age')
    patient_photo_type      = request.form.get('patient_photo_type')
    patient_photo_file      = request.form.get('patient_photo_file')
    patient_diagnois_type   = request.form.get('patient_diagnois_type')
    patient_diagnois_result = request.form.get('patient_diagnois_result')
    
    case.patient_name            = patient_name
    case.patient_gender          = patient_gender
    case.patient_age             = patient_age
    case.patient_photo_type      = patient_photo_type
    case.patient_photo_file      = patient_photo_file
    case.patient_diagnois_type   = patient_diagnois_type
    case.patient_diagnois_result = patient_diagnois_result
    case.is_diagnosed            = 0
    case.doctor_name             = ''
    case.doctor_hospital         = ''
    case.doctor_department       = ''
    case.case_upload_time        = ''
    case.case_diagnois_time      = ''
    case.case_expert_time        = ''
    print(case)
    try:
        # TODO... write into db
        db.session.add(case)
        db.session.commit()
        return jsonify({'result':'success'})
    except:
        return jsonify({'result':'error'})

def source_case_table_infos():
    # TODO... read from db
    # return as json
    data = []
    names = ['香', '草', '瓜', '果', '桃', '梨', '莓', '橘', '蕉', '苹']
    sex = ['男', '女']
    consultResult = ['好', '坏']
    for i in range(1, 10):
        d = {}
        d['id'] = i
        d['userid'] = i
        d['name'] = choice(names) + choice(names)  # 随机选取汉字并拼接
        d['sex'] = choice(sex)
        d['age'] = 20
        d['imgTpye'] = choice(names)
        d['type'] = choice(consultResult)
        d['consultResult'] = choice(consultResult)
        d['commentType'] = choice(consultResult)
        d['uploadDate'] = '2018-04-21'
        d['department'] = choice(names) + choice(names)
        d['hospital'] = choice(sex)
        d['expert'] = choice(names) + choice(names) + choice(sex)
        data.append(d)
    if request.method == 'GET':
        rdata = {'recordsTotal': len(data), 'data': data}
        rtn = jsonify(rdata)
        return rtn

def answer_case_table_infos():
    # TODO... read from db
    # return as json
    data = []
    names = ['香', '草', '瓜', '果', '桃', '梨', '莓', '橘', '蕉', '苹']
    sex = ['男', '女']
    consultResult = ['好', '坏']
    for i in range(1, 10):
        d = {}
        d['id'] = i
        d['description'] = choice(names) + choice(names) + choice(names) + choice(names)
        d['starter'] = choice(names) + choice(names)
        d['hospital'] = choice(sex)
        d['start-date'] = '2018-04-21'
        data.append(d)
    if request.method == 'GET':
        rdata = {'recordsTotal': len(data), 'data': data}
        rtn = jsonify(rdata)
        return rtn

def case_table_infos():
    # TODO... read from db
    # return as json
    data = []
    names = ['香', '草', '瓜', '果', '桃', '梨', '莓', '橘', '蕉', '苹']
    sex = ['男', '女']
    consultResult = ['好', '坏']
    for i in range(1, 10):
        d = {}
        d['id'] = i
        d['userid'] = i
        d['name'] = choice(names) + choice(names)  # 随机选取汉字并拼接
        d['sex'] = choice(sex)
        d['age'] = 20
        d['imgTpye'] = choice(names)
        d['type'] = choice(consultResult)
        d['consultResult'] = choice(consultResult)
        d['commentType'] = choice(consultResult)
        d['uploadDate'] = '2018-04-21'
        data.append(d)
    if request.method == 'GET':
        rdata = {'recordsTotal': len(data), 'data': data}
        rtn = jsonify(rdata)
        return rtn
