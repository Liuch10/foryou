import os

basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'for-you'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

FLAG_CHAIN = False
CONTRACT_ADDRESS = None
DECIMAL = 18
# BANK_ADDRESS = "0x0000"

TOKEN_ABI_FILE = 'static/contract/FoYoToken.abi'
TOKEN_BIN_FILE = 'static/contract/FoYoToken.bin'
CREDIT_SIGNUP = 500.0
CREDIT_UPLOAD = 2.0
CREDIT_REPLY_CONSULTATION = 1.0
CREDIT_DIAGNOSE = 1.0
MAX_CREDIT = 50.0
