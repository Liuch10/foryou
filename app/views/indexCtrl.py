from flask import Response, render_template
from app.models.models import User
from app import db
from flask_login import current_user, login_required

@login_required
def index(page = 1):
	return render_template('index.html', title='Home', posts = [])
