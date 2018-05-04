from flask import Response, render_template, jsonify, request, g, redirect, url_for
from app.models.models import User, Case, ExpertCase, Consultation
from app.utils.forms import CaseForm
from app import db

from flask_login import current_user, login_required
from sqlalchemy import desc


@login_required
def work():
    form = CaseForm()
    return render_template('work.html', form=form, current_user=current_user)


def add_consultation_comment():
    print("add_comment")
    # TODO... update db

    print(request.form)
    msg = request.form.get('msg')
    case_id = int(request.form.get('case_id'))
    g.user = current_user
    upload_user_id = g.user.id if g.user.is_authenticated else 0
    consultation = Consultation(comment_user_id=upload_user_id, case_id=case_id, comment_content=msg);
    try:
        db.session.add(consultation)
        db.session.commit()
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'fail to add comment'})


def comment_history_table_infos():
    print("comment_history_table_infos")
    case_id = int(request.args['case_id'])
    data = []
    consultations = Consultation.query.filter_by(case_id=case_id).order_by(desc(Consultation.comment_time)).all()
    print('len:')
    print(len(consultations))
    for i in range(0, len(consultations)):
        d = {}
        d['id'] = consultations[i].id
        d['doctor'] = 'test'  # consultations[i].commenter.user_name
        d['comment'] = consultations[i].comment_content
        d['date'] = consultations[i].comment_time
        data.append(d)
    if len(data) == 0:
        d = {}
        d['id'] = "none"
        d['doctor'] = "none"
        d['comment'] = "none"
        d['date'] = "none"
        data.append(d)

    # if request.method == 'GET':
    rdata = {'recordsTotal': len(data), 'data': data}
    rtn = jsonify(rdata)
    return rtn


def work_start_consult():
    print("work_start_consult")
    # comment = request.form.get('comment')
    print(request.form)

    if not ('case_id' in request.form):
        return jsonify({'result': '请正确选择案例'})

    case_id = int(request.form.get('case_id'))
    comment_content = request.form.get('comment') if request.form.get('comment') else "未填写"
    case = Case.query.filter_by(id=case_id).first()
    try:
        if case:
            if not case.in_consultant:
                case.in_consultant = True
                case.consultation_message = comment_content
                db.session.add(case)
                db.session.commit()
                return jsonify({'result': '会诊发布成功'})
            else:
                case.consultation_message = comment_content
                db.session.add(case)
                db.session.commit()
                return jsonify({'result': '该病例已经是会诊病例'})
        else:
            return jsonify({'result': 'no case instance' + str(case.id)})
    except:
        print("error")
        return jsonify({'result': 'error'})


def work_update_expert():
    # TODO... update expert_db
    print("work_update_expert")
    if 'case_id' in request.form:
        return jsonify({'result': '请选择'})
    case_id = int(request.form.get('case_id'))
    g.user = current_user
    user_id = g.user.id if g.user.is_authenticated else 0
    expertCase = ExpertCase(original_case_id=case_id,
                            expert_user_id=user_id)
    try:
        db.session.add(expertCase)
        db.session.commit()
        return jsonify({'result': '更新专家资源成功'})
    except:
        return jsonify({'result': '更新专家资源失败'})


def work_upload_case():
    g.user = current_user
    upload_user_id = g.user.id if g.user.is_authenticated else 0
    print(upload_user_id)
    case_patient_name = request.form.get('patient_name') if 'patient_name' in request.form else '匿名'
    case_patient_gender = request.form.get('patient_gender') if 'patient_gender' in request.form else '男'
    case_patient_age = request.form.get('patient_age') if 'patient_age' in request.form else '0'
    case_photo_type = request.form.get('patient_photo_type') if 'patient_photo_type' in request.form else '未知'
    case_diagnose_type = request.form.get(
        'patient_diagnose_type') if 'patient_diagnose_type' in request.form else '未知'

    case_diagnose_result = request.form.get(
        'patient_diagnose_result') if 'patient_diagnose_result' in request.form else "未知"
    case_photo_hash = request.form.get('patient_photo_file') if 'patient_photo_file' in request.form else 'nohash'

    case = Case(upload_user_id=upload_user_id,
                case_patient_name=case_patient_name,
                case_patient_gender=case_patient_gender,
                case_patient_age=case_patient_age,
                case_photo_type=case_photo_type,
                case_diagnose_type=case_diagnose_type,
                case_diagnose_result=case_diagnose_result,
                case_photo_hash=case_photo_hash)
    try:
        # DONE
        upload_check = Case.query.filter_by(case_photo_hash=case_photo_hash).first()
        if upload_check:
            print("already uploaed")
            return jsonify({'result': '该文件已经被发布过'})
        else:
            db.session.add(case)
            db.session.commit()
            print("success")
            return jsonify({'result': 'success', 'token': 3})
    except:
        print("error")
        return jsonify({'result': 'error'})


def source_case_table_infos():
    # TODO... read from db DONE
    # 资源中心
    get_expert = True if (request.args['type'] == 'expert') else False
    print('expert' + str(get_expert))
    g.user = current_user
    user_id = g.user.id if g.user.is_authenticated else 0
    if get_expert:
        expertcases = ExpertCase.query.order_by(desc(ExpertCase.expert_time)).all()
        cases = [case.original_case for case in expertcases]
        users = [case.expert for case in expertcases]
    else:
        cases = Case.query.order_by(desc(Case.case_upload_time)).all()
        users = [case.uploader for case in cases]

    data = []
    for i in range(1, len(cases)):
        d = {}
        ownership = True if (int(user_id) == int(cases[i].upload_user_id)) else 0
        share = True if (users[i] and users[i].allow_share) else False
        try:
            d['id'] = cases[i].id
            d['userid'] = cases[i].id
            d['name'] = cases[i].case_patient_name if (ownership and share) else "*"
            d['sex'] = cases[i].case_patient_gender if (ownership and share) else "*"
            d['age'] = cases[i].case_patient_age if (ownership and share) else "*"
            d['imgTpye'] = cases[i].case_photo_type if (ownership and share) else "*"
            d['type'] = cases[i].case_diagnose_type if (ownership and share) else "*"
            d['consultResult'] = cases[i].case_diagnose_result if (ownership and share) else "*"
            d['commentType'] = cases[i].is_tagged if (ownership and share) else "*"
            d['uploadDate'] = cases[i].case_upload_time if (ownership and share) else "*"
        except:
            d['id'] = "-1"
            d['userid'] = "-2"
            d['name'] = "default_id"
            d['sex'] = "*"
            d['age'] = "0"
            d['imgTpye'] = "*"
            d['type'] = "*"
            d['consultResult'] = "*"
            d['commentType'] = "*"
            d['uploadDate'] = "*"
        try:
            d['department'] = users[i].user_department if (ownership and share) else "*"
            d['hospital'] = users[i].user_hospital if (ownership and share) else "*"
            d['expert'] = users[i].user_name if (ownership and share) else "*"
        except:

            d['department'] = 'default_depart'
            d['hospital'] = 'default_hos'
            d['expert'] = 'default_expert'

        data.append(d)
    if request.method == 'GET':
        rdata = {'recordsTotal': len(data), 'data': data}
        rtn = jsonify(rdata)
        return rtn


def answer_case_table_infos():
    # TODO... read from consultant_db
    # 接收会诊
    # return as json
    print("answer-case_table-info")
    consultant_cases = Case.query.filter_by(in_consultant=True).order_by(desc(Case.consultant_time)).all()
    print(len(consultant_cases))
    g.user = current_user
    data = []
    if (not g.user.is_authenticated):
        rdata = {'recordsTotal': 0, 'data': []}
        return jsonify(rdata)
    for i in range(0, len(consultant_cases)):
        d = {}
        ownership = True if (consultant_cases[i].upload_user_id == g.user.id) else False
        d['id'] = consultant_cases[i].id
        d['description'] = consultant_cases[i].consultation_message
        d['starter'] = consultant_cases[i].upload_user_id if ownership else '*'
        d['hospital'] = "test" if ownership else '*'
        d['department'] = "test" if ownership else '*'
        d['start-date'] = "test" if ownership else '*'
        data.append(d)
    if request.method == 'GET':
        rdata = {'recordsTotal': len(data), 'data': data}
        rtn = jsonify(rdata)
        return rtn


def Case2Json(case, secret=False):
    d = {}
    d['id'] = case.id
    d['userid'] = case.id
    d['name'] = case.case_patient_name if (not secret) else "****"
    d['sex'] = case.case_patient_gender if (not secret) else "****"
    d['age'] = case.case_patient_age if (not secret) else "****"
    d['imgTpye'] = case.case_photo_type if (not secret) else "****"
    d['type'] = case.case_diagnose_type if (not secret) else "****"
    d['consultResult'] = case.case_diagnose_result if (not secret) else "****"
    commentType = "已标注" if case.is_tagged else "未标注"
    d['commentType'] = commentType if (not secret) else "****:w"
    d['uploadDate'] = case.case_upload_time if (not secret) else "****"
    d['hospital'] = "***"
    return d


def case_table_infos():
    # TODO... read from  DONE
    g.user = current_user
    user_id = g.user.id if g.user.is_authenticated else 0
    cases = Case.query.filter_by(upload_user_id=user_id).order_by(desc(Case.case_upload_time)).all()
    data = []
    for i in range(0, len(cases)):
        data.append(Case2Json(cases[i]))
    if request.method == 'GET':
        rdata = {'recordsTotal': len(data), 'data': data}
        rtn = jsonify(rdata)
        return rtn


def update_personal_info():
    print("update_personal_info")
    print(request.form)
    g.user = current_user
    user_authenticated = g.user.is_authenticated
    if user_authenticated and request.method == 'POST':
        try:
            g.user.user_name = request.form.get('name')
            g.user.user_age = request.form.get('age')
            g.user.user_hospital = request.form.get('hospital')
            g.user.user_department = request.form.get('department')
            g.user.user_title = request.form.get('title')
            g.user.telephone = request.form.get('telephone')
            g.user.user_city = request.form.get('province')
            g.user.user_mail = request.form.get('mail')
            g.user.allow_share = True if (request.form.get('allowshare') == '是') else False
            db.session.add(g.user)
            db.session.commit()
            return jsonify({'result': '修改成功'})
        except:
            return jsonify({'result': "failed to update personal info"})
    else:
        rdata = {'name': g.user.user_name if user_authenticated else "notlogin",
                 'age': g.user.user_age if user_authenticated else "-1",
                 'hospital': g.user.user_hospital if user_authenticated else "notlogin",
                 'title': g.user.user_title if user_authenticated else "notlogin",
                 'telephone': g.user.user_phone if user_authenticated else "notlogin",
                 'province': g.user.user_city if user_authenticated else "",
                 'mail': g.user.user_mail if user_authenticated else "notlogin",
                 'department': g.user.user_department if user_authenticated else "notlogin",
                 'allowshare': '是' if user_authenticated and g.user.allow_share  else "否"}
    # print(rdata)
    return jsonify(rdata)


def reply_consultation():
    # TODO get case_id and comment content from frontend
    case_id = 0
    comment_content = ""
    g.user = current_user
    comment_user_id = g.user.id if g.user.is_authenticated else 0
    consult = Consultation(comment_user_id=comment_user_id,
                           case_id=case_id,
                           comment_content=comment_content)
    try:
        db.session.add(consult)
        db.session.commit()
        return jsonify({'result': '回复成功'})
    except:
        return jsonify({'result': '恢复失败'})


def get_image_address():
    case_id = int(request.form.get('id'))
    case = Case.query.filter_by(id=case_id).first()
    # return jsonify({'result': 'success', 'address': "QmWo5Pgo3WAXZfTCNtuGgruafmQY13eSCCm4aNeZycVknE"})
    if current_user.is_authenticated and case and case.upload_user_id == current_user.id:
        addr = case.case_photo_hash
        return jsonify({'result': 'success', 'address': addr})
    else:
        addr = 'invalid user'
        return jsonify({'result': 'error', 'address': addr})


def get_consultation_message():
    print("consultation_message")
    case_id = int(request.form.get('id'))
    case = Case.query.filter_by(id=case_id).first()
    print(case_id)
    if current_user.is_authenticated and case and case.upload_user_id == current_user.id:
        message = case.consultation_message
        return jsonify({'result': 'success', 'address': message})
    else:
        message = 'invalid'
        return jsonify({'result': 'error', 'message': message})
