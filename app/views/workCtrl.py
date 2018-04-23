from flask import Response, render_template, jsonify, request
from app.models.models import User, Case
from app.utils.forms import CaseForm
from app import db
from random import choice
from flask_login import current_user, login_required



# @login_required
def work():
    form = CaseForm()
    return render_template('work.html', form=form)


def work_start_comment():
    comment = request.form.get('comment')
    # TODO... update db
    return jsonify({'result': 'success'})


def work_start_consult():
    comment = request.form.get('comment')
    # TODO... update db
    return jsonify({'result': 'success'})


def work_update_expert():
    comment = request.form.get('comment')
    # TODO... update db
    return jsonify({'result': 'success'})


def work_upload_case():
    print("hrere")
    case_patient_name = request.form.get('patient_name')
    case_patient_gender = request.form.get('patient_gender')
    case_patient_age = request.form.get('patient_age')
    case_photo_type = request.form.get('patient_photo_type')
    case_diagnose_type = request.form.get('patient_diagnois_type')
    case_diagnose_result = request.form.get('patient_diagnois_result')
    case_photo_hash = request.form.get('patient_photo_file')

    case = Case(case_patient_name=case_patient_name,
                case_patient_gender=case_patient_gender,
                case_patient_age=case_patient_age,
                case_photo_type=case_photo_type,
                case_diagnose_type=case_diagnose_type,
                case_diagnose_result=case_diagnose_result,
                case_photo_hash=case_photo_hash)
    try:
        # DONE
        print(case)
        print(case_photo_hash)
        upload_check = Case.query.filter_by(case_photo_hash=case_photo_hash).first()
        if (upload_check):
            print("this photo has been uploaded")
            return jsonify({'result': 'error'})
        else:
            db.session.add(case)
            db.session.commit()
            print("success")
            return jsonify({'result': 'success'})
    except:
        print("error")
        return jsonify({'result': 'error'})


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
