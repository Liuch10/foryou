from flask import render_template, flash, url_for, session, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from app.utils.forms import LoginForm, SignUpForm
from app.utils.sendmail import send_mail
from app.models.models import User
from app import app, db
from datetime import datetime

from mailer import Mailer
from mailer import Message
from random import randint

import hashlib
import json
import sys


def getPasswordHash(passphrase):
    md5 = hashlib.md5()
    md5.update(passphrase.encode('utf-8'))
    return md5.hexdigest()


def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login_check(request.form.get('user_mail'),
                                getPasswordHash(request.form.get('user_password')))
        if user:
            login_user(user)
            user.last_seen = datetime.now()
            try:
                db.session.add(user)
                db.session.commit()
            except:
                print("The Database error!")
                return redirect('/login')
            # flash('Your name: ' + request.form.get('user_name'))
            print("login success")
            return redirect(url_for("index"))
        else:
            print('Login failed, usermail or password error!')
            return redirect('/login')
    print(form.errors)
    return render_template('login.html', form=form)


def sign_up():
    form = SignUpForm(request.form)
    print(form.data)
    if form.validate_on_submit():
        user = User()
        user_mail = request.form.get('user_mail')
        # user_name = request.form.get('user_name')
        user_password = getPasswordHash(request.form.get('user_password'))
        user_type = request.form.get('user_type') or ""
        user_city = request.form.get('user_city') or ""
        user_hospital = request.form.get('user_hospital') or ""
        user_department = request.form.get('user_department') or ""
        user_phone = request.form.get('user_phone') or ""
        # user_chain_address = request.form.get('user_chain_address') or ""
        register_check = User.query.filter(db.and_(User.user_mail == user_mail,
                                                   User.user_password == user_password)).first()
        if register_check:
            print("user exists")
            return redirect('/sign-up')
        if (len(user_mail) and len(user_password) and
                ('verification_code' in session) and
                (session['verification_code'] == request.form.get('user_verification_code'))):
            user.user_mail = user_mail
            user.user_password = user_password
            user.user_type = user_type
            user.user_city = user_city
            user.user_hospital = user_hospital
            user.user_department = user_department
            user.user_phone = user_phone
            # user.user_chain_address = user_chain_address
            user.user_reg_time = datetime.now()
            try:
                db.session.add(user)
                db.session.commit()
            except:
                print("db error")
                return redirect('/sign-up')
            print(user_mail + ":" + user_password)
            return render_template("signup_success.html")
    print(form.errors)
    return render_template("signup.html", form=form)


def sendMail():
    try:
        receiver = json.loads(request.form.get('data')).get('user_mail')

        code = ''.join(["%s" % randint(0, 9) for _ in range(0, 6)])

        session['verification_code'] = code
        if (send_mail(recv=receiver, content=code)):
            # response ajax for front end
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
