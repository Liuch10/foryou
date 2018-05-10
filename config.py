import os

basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'for-you'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

FLAG_CHAIN = False
CONTRACT_ADDRESS = "0xeb318dc01C835CB01E627215cB67e3a2e0Bc90D5"
DECIMAL = 18
# BANK_ADDRESS = "0x0000"

TOKEN_ABI_FILE = 'app/static/contract/FoYoToken.abi'
TOKEN_BIN_FILE = 'app/static/contract/FoYoToken.bin'
CREDIT_SIGNUP = 500.0
CREDIT_UPLOAD = 1.0
CREDIT_REPLY_CONSULTATION = 0.5
CREDIT_DIAGNOSE = 0.5
MAX_CREDIT = 100.0
