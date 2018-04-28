from flask import Response, render_template, jsonify, request, g, redirect, url_for
from app.models.models import User, Case, ExpertCase, Consultation
from app.utils.forms import DiagnoseForm
from app import db
from datetime import datetime
from flask_login import current_user, login_required
from sqlalchemy import desc


def diagnose():
    g.user = current_user

    # ownership = True if (g.user.is_authenticated and int(g.user.id) == int(request_case.upload_user_id)) else False
    ownership = True

    if request.method == 'GET':
        if ownership:
            case_id = (request.args.get('id'))
            request_case = Case.query.filter_by(id=case_id).first()
            form = DiagnoseForm(case_id=case_id,
                                case_patient_age=request_case.case_patient_age if request_case else "0")
            return render_template("diagnose.html", form=form)
        else:
            return redirect(url_for('work'))
    elif request.method == "POST":
        ##TODO WRITE to DB
        specs = str(request.form)
        case_id = int(request.form.get('case_id'))
        request_case = Case.query.filter_by(id=case_id).first()
        request_case.is_tagged = True
        request_case.case_tag_info = specs
        request_case.case_tag_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                       '%Y-%m-%d %H:%M:%S')
        try:
            db.session.add(request_case)
            db.session.commit()
            return jsonify({'result': 'success'})
        except:
            return jsonify({'result': 'error'})
