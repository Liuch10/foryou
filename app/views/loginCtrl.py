from flask import render_template, flash, url_for, session, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from app.utils.forms import LoginForm, SignUpForm
from app.models.models import User
from app import app, db
import hashlib
from datetime import datetime

def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login_check(request.form.get('user_name'), 
            request.form.get('user_password'))
        if user:
            login_user(user)
            user.last_seen = datetime.now()
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                return redirect('/login')
            flash('Your name: ' + request.form.get('user_name'))
            return redirect(url_for("index"))
        else:
            flash('Login failed, username or password error!')
            return redirect('/login')
    return render_template('login.html', form = form)

def sign_up():
    form = SignUpForm()
    user = User()
    if form.validate_on_submit():
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        user_type = request.form.get('user_type') or ""
        user_city = request.form.get('user_city') or ""
        user_hospital = request.form.get('user_hospital') or ""
        user_department = request.form.get('user_department') or ""
        user_phone = request.form.get('user_phone') or ""
        user_chain_address = request.form.get('user_chain_address') or ""
        register_check = User.query.filter(db.and_(User.user_name == user_name, 
            User.user_password == user_password)).first()
        if register_check:
            return redirect('/sign-up')
        if len(user_name) and len(user_password):
            user.user_name = user_name
            user.user_password = user_password
            user.user_type = user_type
            user.user_city = user_city
            user.user_hospital = user_hospital
            user.user_department = user_department
            user.user_phone = user_phone
            user.user_chain_address = user_chain_address
            user.user_reg_time = datetime.now()
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return redirect('/sign-up')
        return redirect('/index')
    return render_template("sign_up.html", form = form)

@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
