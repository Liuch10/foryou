import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from config import basedir

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

from app.views import views
from app.models import models
