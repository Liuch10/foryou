from flask import render_template, flash, url_for, session, redirect, request
from app.utils.forms import uploadCaseForm
from flask_login import login_required
from werkzeug.utils import secure_filename


# @login_required
def upload_case():
    form = uploadCaseForm()
    if form.validate_on_submit():
        print(form.patient_photo_file.data)
        return redirect(url_for('index'))
    print(form.errors)
    return render_template('upload_case.html', form=form)
