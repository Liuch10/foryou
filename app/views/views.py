from flask import g
from flask_login import current_user
from datetime import datetime

from app import app, db, lm
from app.models.models import User
from app.views.mainCtrl import main, contactUs, aboutUs, product
from app.views.loginCtrl import login, sign_up, logout, sendMail, sign_up_success
from app.views.workCtrl import work, case_table_infos, work_upload_case, work_start_consult, answer_case_table_infos, \
    source_case_table_infos, work_update_expert, add_consultation_comment, update_personal_info, get_image_address, \
    comment_history_table_infos, get_consultation_message, get_balance
from app.views.diagnoseCtrl import diagnose
from app.views.wallet import check_wallet


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


# app.add_url_rule('/', methods=['GET'], view_func = index)
app.add_url_rule('/foryou', methods=['GET'], view_func=main)
app.add_url_rule('/main', methods=['GET'], view_func=main)
app.add_url_rule('/', methods=['GET'], view_func=main)
app.add_url_rule('/about-us', methods=['GET'], view_func=aboutUs)
app.add_url_rule('/product', methods=['GET'], view_func=product)
app.add_url_rule('/contact-us', methods=['GET'], view_func=contactUs)
app.add_url_rule('/login', methods=['GET', 'POST'], view_func=login)
app.add_url_rule('/sign-up', methods=['GET', 'POST'], view_func=sign_up)
# app.add_url_rule('/sign-up', methods=['GET', 'POST'], view_func=main)
app.add_url_rule('/sign-up-success', methods=['GET'], view_func=sign_up_success)
app.add_url_rule('/sendMail', methods=['POST'], view_func=sendMail)
app.add_url_rule('/work', methods=['GET'], view_func=work)
app.add_url_rule('/case-table-infos', methods=['GET'], view_func=case_table_infos)
app.add_url_rule('/answer-case-table-infos', methods=['GET'], view_func=answer_case_table_infos)
app.add_url_rule('/case-table-source-infos', methods=['GET'], view_func=source_case_table_infos)
app.add_url_rule('/comment-history-table-infos', methods=['GET'], view_func=comment_history_table_infos)

# 退出登陆
app.add_url_rule('/logout', methods=['GET', 'POST'], view_func=logout)
# 上传病例
app.add_url_rule('/upload_case', methods=['POST'], view_func=work_upload_case)
# 发起会诊
app.add_url_rule('/start_consult', methods=['POST'], view_func=work_start_consult)
# 更新专家
app.add_url_rule('/update_expert', methods=['POST'], view_func=work_update_expert)
# 开始标注
app.add_url_rule('/diagnose', methods=['GET', 'POST'], view_func=diagnose)

# 会诊添加回复
app.add_url_rule('/addConsultationComment', methods=['GET', 'POST'], view_func=add_consultation_comment)

# 修改资料
app.add_url_rule('/updatePersonalInfo', methods=['POST', 'GET'], view_func=update_personal_info)
# 上传病例
app.add_url_rule('/wallet-table-infos', methods=['GET'], view_func=check_wallet)

app.add_url_rule('/getImageAddress', methods=['POST'], view_func=get_image_address)
#
# app.add_url_rule('/upload-case', methods=['POST','GET'], view_func=upload_case)

app.add_url_rule('/getConsultationMessage', methods=['POST'], view_func=get_consultation_message)

app.add_url_rule('/get-balance', methods=['GET'], view_func=get_balance)
