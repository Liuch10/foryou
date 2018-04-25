from flask import Response, render_template, jsonify, request, g
from app.models.models import User, Case, ExpertCase, Consultation
from app.utils.forms import CaseForm
from app import db

from flask_login import current_user, login_required
from sqlalchemy import desc


# @login_required
def work():
    form = CaseForm()
    return render_template('work.html', form=form)


def work_start_comment():
    print("work_start_comment")
    comment = request.form.get('comment')
    # TODO... update db
    return jsonify({'result': 'success'})


def work_start_consult():
    print("work_start_consult")
    # comment = request.form.get('comment')
    # TODO... update consult_db # DONE

    case_id = request.form.get('case_id') if request.form.get('case_id') else 8
    print(case_id)
    comment_content = request.form.get('comment') if request.form.get('comment') else "unknown"
    print(comment_content)
    case = Case.query.filter_by(id=case_id).first()
    print(case)
    try:
        if case:
            if (not case.in_consultant):
                case.in_consultant = True
                case.consultation_message = comment_content
                db.session.add(case)
                db.session.commit()
                print(case.consultation_message)
                return jsonify({'result': 'success'})
            else:
                case.consultation_message = comment_content
                db.session.add(case)
                db.session.commit()
                print(case.consultation_message)
                print("already")
                return jsonify({'result': 'already in consultation'})
        else:
            return jsonify({'result': 'no case instance' + str(case.id)})
    except:
        print("error")
        return jsonify({'result': 'error'})


def work_update_expert():
    # TODO... update expert_db
    print(request.data)
    print("work_update_expert")
    case_id = request.form.get('case_id') if request.form.get('case_id') else 0  # js error in getSelected in the js
    expertCase = ExpertCase(original_case_id=case_id,
                            expert_user_id=0)
    try:
        db.session.add(expertCase)
        db.session.commit()
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'error'})


def work_upload_case():
    print(request.form)
    case_patient_name = request.form.get('patient_name')
    case_patient_gender = request.form.get('patient_gender')
    case_patient_age = request.form.get('patient_age')
    case_photo_type = request.form.get('patient_photo_type')
    case_diagnose_type = request.form.get('patient_diagnose_type')
    case_diagnose_result = request.form.get('patient_diagnose_result')
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
        print(case.case_photo_hash)
        # print(case_photo_hash)
        upload_check = Case.query.filter_by(case_photo_hash=case_photo_hash).first()
        if (upload_check):
            print("this photo has been uploaded")
            return jsonify({'result': 'this photo has been uploaded'})
        else:
            db.session.add(case)
            db.session.commit()
            print("success")
            return jsonify({'result': 'success'})
    except:
        print("error")
        return jsonify({'result': 'error'})


def source_case_table_infos():
    # TODO... read from db DONE
    # return as json
    # 资源中心
    print(request.args)
    get_expert = True if (request.args['type'] == 'expert') else False
    if get_expert:
        expertcases = ExpertCase.query.order_by(desc(ExpertCase.expert_time)).all()
        cases = [case.original_case for case in expertcases]
        users = [case.expert for case in expertcases]
        print('here')
        # print(len(cases))
    else:
        cases = Case.query.order_by(desc(Case.case_upload_time)).all()
        print(cases)
        users = [case.user for case in cases]
        print(len(cases))

    data = []
    for i in range(1, len(cases)):
        d = {}
        try:
            d['id'] = cases[i].id
            d['userid'] = cases[i].id
            d['name'] = cases[i].case_patient_name  # choice(names) + choice(names)  # 随机选取汉字并拼接
            d['sex'] = cases[i].case_patient_gender
            d['age'] = cases[i].case_patient_age
            d['imgTpye'] = cases[i].case_photo_type
            d['type'] = cases[i].case_diagnose_type
            d['consultResult'] = cases[i].case_diagnose_result
            d['commentType'] = cases[i].is_tagged
            d['uploadDate'] = cases[i].case_upload_time
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
            d['department'] = users[i].user_department
            d['hospital'] = users[i].user_hospital
            d['expert'] = users[i].user_name
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
    consultant_cases = Case.query.filter_by(in_consultant=True).order_by(desc(Case.consultant_time)).all()

    print("answer_case_table_infos:" + str(len(consultant_cases)))
    data = []
    for i in range(1, len(consultant_cases)):
        d = {}
        d['id'] = consultant_cases[i].id
        d['description'] = consultant_cases[i].consultation_message
        print(str(consultant_cases[i].id) + ":" + str(consultant_cases[i].consultation_message))
        d['starter'] = consultant_cases[i].upload_user_id
        d['hospital'] = "test"
        d['department'] = "test"
        d['start-date'] = "test"
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
    cases = Case.query.order_by(desc(Case.case_upload_time)).all()
    data = []

    for i in range(1, len(cases)):
        data.append(Case2Json(cases[i]))
    if request.method == 'GET':
        rdata = {'recordsTotal': len(data), 'data': data}
        rtn = jsonify(rdata)
        return rtn


def update_personal_info():
    print("update_personal_info")
    print(request.form)

    g.user = current_user
    if request.method == 'POST':
        try:
            g.user.user_name = request.form.get('name')
            g.user.age = request.form.get('age')
            g.user.user_hospital = request.form.get('hospital')
            g.user.user_department = request.form.get('department')
            g.user.user_title = request.form.get('title')
            g.user.telephone = request.form.get('telephone')
            g.user.user_city = request.form.get('province')
            g.user.user_mail = request.form.get('mail')
            g.user.allow_share = True if (request.form.get('share') == '是') else False
            db.session.add(g.user)
            db.session.commit()
            return jsonify({'result': '修改成功'})
        except:
            return jsonify({'result': "failed to update personal info"})
    else:
        rdata = {'name': g.user.user_name,
                 'age': g.user.age,
                 'hospital': g.user.user_hospital,
                 'title': g.user.user_title,
                 'telephone': g.user.telephone,
                 'province': g.user.user_city,
                 'mail': g.user.user_mail}
        return jsonify(rdata)


def update_personal_info():
    print("update_personal_info")
    print(request.form)
    g.user = current_user
    user_authenticated = g.user.is_authenticated
    if user_authenticated and request.method == 'POST':
        try:
            g.user.user_name = request.form.get('name')
            g.user.age = request.form.get('age')
            g.user.user_hospital = request.form.get('hospital')
            g.user.user_department = request.form.get('department')
            g.user.user_title = request.form.get('title')
            g.user.telephone = request.form.get('telephone')
            g.user.user_city = request.form.get('province')
            g.user.user_mail = request.form.get('mail')
            g.user.allow_share = True if (request.form.get('share') == '是') else False
            db.session.add(g.user)
            db.session.commit()
            return jsonify({'result': '修改成功'})
        except:
            return jsonify({'result': "failed to update personal info"})
    else:
        rdata = {'name': g.user.user_name if user_authenticated else "notlogin",
                 'age': g.user.age if user_authenticated else "-1",
                 'hospital': g.user.user_hospital if user_authenticated else "notlogin",
                 'title': g.user.user_title if user_authenticated else "notlogin",
                 'telephone': g.user.telephone if user_authenticated else "notlogin",
                 'province': g.user.user_city if user_authenticated else "",
                 'mail': g.user.user_mail if user_authenticated else "notlogin",
                 'department': g.user.user_department if user_authenticated else "notlogin",
                 'share': g.user.allow_share if user_authenticated else ""}

    return jsonify(rdata)
