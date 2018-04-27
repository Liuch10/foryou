from flask import jsonify, g
from flask_login import current_user, login_required
from sqlalchemy import desc


def check_wallet():
    print('check_wallet')
    g.user = current_user
    data = []
    if g.user.is_authenticated:
        trans = g.user.transactionss
        for i in range(1, len(trans)):
            d = {}
            d['id'] = i
            d['date'] = trans[i].trans_time
            d['type'] = trans[i].trans_type
            d['amount'] = trans[i].trans_amount
            d['spec'] = trans[i].trans_spec
            data.append(d)
    else:
        d = {}
        d['id'] = 0
        d['date'] = 'undefined'
        d['type'] = 'undefined'
        d['amount'] = 'undefined'
        d['spec'] = 'undefined'
        data.append(d)
    rdata = {'recordsTotal': len(data), 'data': data}
    rtn = jsonify(rdata)
    return rtn
