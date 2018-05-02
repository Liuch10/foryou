import os

basedir = os.path.abspath(os.path.dirname(__file__))
SRF_ENABLED = True
SECRET_KEY = 'for-you'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

TOKEN_ABI_FILE = 'static/contract/FoYoToken.abi'
TOKEN_BIN_FILE = 'static/contract/FoYoToken.bin'
CONTRACT_ADDRESS = None
