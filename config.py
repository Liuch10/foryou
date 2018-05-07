import os

basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'for-you'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

FLAG_CHAIN = True
CONTRACT_ADDRESS = None
TOKEN_ABI_FILE = 'static/contract/FoYoToken.abi'
TOKEN_BIN_FILE = 'static/contract/FoYoToken.bin'
DECIMAL = 18
CREDIT_SIGNUP = 1
CREDIT_UPLOAD = 1
CREDIT_REPLY_CONSULTATION = 1
