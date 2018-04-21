from flask import g
from flask_login import current_user
from datetime import datetime

from app import app, db, lm
from app.models.models import User
from app.views.indexCtrl import index
from app.views.mainCtrl import main, contactUs, aboutUs, product
from app.views.loginCtrl import login, sign_up, logout, sendMail
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
app.add_url_rule('/main', methods=['GET'], view_func = main)
app.add_url_rule('/about-us', methods=['GET'], view_func = aboutUs)
app.add_url_rule('/product', methods=['GET'], view_func = product)
app.add_url_rule('/contact-us', methods=['GET'], view_func = contactUs)
app.add_url_rule('/login', methods=['GET', 'POST'], view_func=login)
app.add_url_rule('/sign-up', methods=['GET', 'POST'], view_func=sign_up)
app.add_url_rule('/sendMail', methods=['POST'], view_func=sendMail)
# app.add_url_rule('/logout', methods=['GET'], view_func = logout)
#
# app.add_url_rule('/upload-case', methods=['POST','GET'], view_func=upload_case)
