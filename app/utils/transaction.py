from flask import g
from flask_login import current_user
from app.models.models import Transaction, Wage
from app import db
from config import MAX_CREDIT
from config import FLAG_CHAIN
from datetime import datetime
from app import contract_helper


def tryCredit(user_id, num, trans_type, spec, restricted=True):
    # todo
    # return the amount to credit

    # user_id = current_user.id if current_user.is_authenticated else 0

    print("tryCredit")
    today = datetime.now().strftime('%Y%m%d')
    user_wage = Wage.query.filter_by(user_id=user_id).filter_by(wage_date=today).first()
    # user_wage=None
    print(user_wage)
    if user_wage is not None:
        available_credit = min(MAX_CREDIT - user_wage.wage, num)
    else:
        user_wage = Wage(user_id=user_id, wage=0.0, wage_date=today)
        print(user_wage)
        if restricted:
            available_credit = min(MAX_CREDIT, num)
        else:
            available_credit = num
    print(available_credit)
    print("available")
    try:
        # update wage
        if restricted:
            user_wage.wage += available_credit
        db.session.add(user_wage)
        db.session.commit()
        print("commit")
        # update transaction
        if FLAG_CHAIN:
            trans_hash = contract_helper.reward(user_id, num)
        else:
            trans_hash = "0x00"
        print("hash")
        print(trans_hash)
        user_trans = Transaction(user_id=user_id,
                                 trans_amount=available_credit,
                                 trans_type=trans_type,
                                 trans_spec=spec,
                                 trans_hash=trans_hash)
        db.session.add(user_trans)
        db.session.commit()

        return available_credit

    except:
        return 0
