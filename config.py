import os
basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'for-you'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

MAIL_HOST = "smtp.163.com"
MAIL_PORT = 465
MAIL_ADD = "foryou_official@163.com"
MAIL_PW = "abcd1234"
