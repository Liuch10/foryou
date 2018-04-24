from flask import g
from flask_login import current_user
from app.models.models import Transaction
from app import db
from config import BANK_USER_ID, BANK_WALLET_ADDRESS


def trans(num_token, type='system', spec="system transaction"):
    # g.user = current_user
    if (num_token == 0):
        return False
        # earn
    g.user.user_wallet_balance += num_token
    user_trans = Transaction(user_id=g.user.id,
                             trans_amount=num_token,
                             trans_type=type,
                             trans_spec=spec)
    sys_trans = Transaction(user_id=BANK_USER_ID,
                            trans_amount=num_token * (-1),
                            trans_type=g.user.id)
    try:
        db.session.add(g.user)
        db.session.add(user_trans)
        db.session.add(sys_trans)
        db.session.commit()
        return True
    except:
        return False


def transContract(from_add, passphrase, to_add, amount):
    return True
