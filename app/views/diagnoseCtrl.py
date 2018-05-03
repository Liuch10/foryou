from flask import Response, render_template, jsonify, request, g, redirect, url_for
from app.models.models import User, Case, ExpertCase, Consultation
from app.utils.forms import DiagnoseForm
from app import db
from datetime import datetime
from flask_login import current_user, login_required
import json
from sqlalchemy import desc


def diagnose():
    print("标注")
    g.user = current_user

    # ownership = True

    if request.method == 'GET':
        case_id = int(request.args.get('id'))
        print(case_id)
        request_case = Case.query.filter_by(id=case_id).first()
        ownership = True if (g.user.is_authenticated and int(g.user.id) == int(request_case.upload_user_id)) else False
        if ownership:
            if not request_case.is_tagged:
                # not diagnosed
                form = DiagnoseForm(case_id=case_id)
                return render_template("diagnose.html", form=form)
            else:
                # already diagnosed
                print(request_case.case_tag_info)
                form = DiagnoseForm.build_form_from_json_string(request_case.case_tag_info)
                # form = DiagnoseForm(case_id=case_id)
                return render_template("diagnose.html", form=form, case_patient_age=request_case.case_patient_age)
        else:
            return redirect(url_for('work'))
    elif request.method == "POST":
        ##TODO WRITE to DB
        specs = json.dumps(request.form)
        print(specs)
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
