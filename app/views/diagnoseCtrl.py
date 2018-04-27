from flask import Response, render_template, jsonify, request, g, redirect, url_for
from app.models.models import User, Case, ExpertCase, Consultation
from app.utils.forms import DiagnoseForm
from app import db

from flask_login import current_user, login_required
from sqlalchemy import desc


def diagnose():
    case_id = 0
    request_case = Case.query.filter_by(id=case_id).first()
    g.user = current_user

    ownership = True if (g.user.is_authenticated and int(g.user.id) == int(request_case.upload_user_id)) else False
    # ownership = True

    if request.method == 'GET':
        if ownership:
            form = DiagnoseForm()
            return render_template("diagnose.html", form=form)
        else:
            return redirect(url_for('work'))
    elif request.method == "POST":
        ##TODO WRITE to DB
        return jsonify({'result': 'error'})
