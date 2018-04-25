import os

basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'for-you'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

BANK_USER_ID = 0
BANK_WALLET_ADDRESS = "0000"
