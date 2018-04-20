from flask import g
from flask_login import current_user
from datetime import datetime

from app import app, db, lm
from app.models.models import User
from app.views.indexCtrl import index
from app.views.loginCtrl import login, sign_up, logout
from app.views.uploadCtrl import upload_case

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

# app.add_url_rule('/', methods=['GET'], view_func = index)
# app.add_url_rule('/index', methods=['GET'], view_func = index)
app.add_url_rule('/login', methods=['GET', 'POST'], view_func=login)
# app.add_url_rule('/sign-up', methods=['GET','POST'], view_func = sign_up)
# app.add_url_rule('/logout', methods=['GET'], view_func = logout)
#
# app.add_url_rule('/upload-case', methods=['POST','GET'], view_func=upload_case)
