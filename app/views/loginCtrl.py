from flask import render_template, flash, url_for, session, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from app.utils.forms import LoginForm, SignUpForm
from app.models.models import User
from app import app, db
from datetime import datetime

def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.login_check(request.form.get('username'),request.form.get('password'))
		if user:
			login_user(user)
			user.last_seen = datetime.now()
			try:
				db.session.add(user)
				db.session.commit()
			except:
				flash("The Database error!")
				return redirect('/login')
			flash('Your name: ' + request.form.get('username'))
			return redirect(url_for("index"))
		else:
			flash('Login failed, username or password error!')
			return redirect('/login')
	return render_template('login.html',form=form)

def sign_up():
	form = SignUpForm()
	user = User()
	if form.validate_on_submit():
		user_name = request.form.get('username')
		user_password = request.form.get('password')
		register_check = User.query.filter(db.and_(User.username == user_name, User.password == user_password)).first()
		if register_check:
			return redirect('/sign-up')
		if len(user_name) and len(user_password):
			user.username = user_name
			user.password = user_password
		try:
			db.session.add(user)
			db.session.commit()
		except:
			return redirect('/sign-up')
		return redirect('/index')
	return render_template("sign_up.html",form=form)

@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))