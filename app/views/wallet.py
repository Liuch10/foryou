from flask import jsonify, g
from flask_login import current_user, login_required
from sqlalchemy import desc
from app.models.models import Transaction

def check_wallet():
    print('check_wallet')
    g.user = current_user
    data = []
    if g.user.is_authenticated and len(g.user.transactions) > 0:
        trans = g.user.transactions
        for i in range(0, len(trans)):
            d = {}
            d['id'] = i
            d['date'] = trans[i].trans_time.strftime('%Y-%m-%d %H:%M:%S')
            d['trans_hash'] = trans[i].trans_hash
            d['type'] = trans[i].trans_type
            d['amount'] = trans[i].trans_amount if trans[i].trans_amount<0 else "+"+str(trans[i].trans_amount)
            d['spec'] = trans[i].trans_spec
            data.append(d)
    else:
        d = {}
        d['id'] = 0
        d['date'] = '无'
        d['type'] = '无'
        d['amount'] = '无'
        d['spec'] = '无'
        data.append(d)
    rdata = {'recordsTotal': len(data), 'data': data}
    rtn = jsonify(rdata)
    return rtn
