from flask import Response, render_template
from app.models.models import User
from app import db
from flask_login import current_user, login_required

@login_required
def index(page = 1):
	# posts = Post.query.filter_by(user_id = current_user.id).order_by(db.desc(Post.time)).paginate(page,3, False)
	# return render_template('index.html', title='Home', posts = [])
	return Response('<p>hello</p>')