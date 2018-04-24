from app import db
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_mail = db.Column(db.String(64), unique=True, default="test@test.com")
    user_password = db.Column(db.String(64), default="default")
    user_name = db.Column(db.String(64), default="default")
    user_age = db.Column(db.String(64), default="default")
    user_type = db.Column(db.String(64), default="doctor")
    user_city = db.Column(db.String(64), default="default")
    user_hospital = db.Column(db.String(64), default="default")
    user_department = db.Column(db.String(64), default="default")
    user_title = db.Column(db.String(64), default="default")
    user_phone = db.Column(db.String(64), default="1234567890")
    user_chain_address = db.Column(db.String(64), default="default")
    user_reg_time = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                     '%Y-%m-%d %H:%M:%S'))
    is_expert = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                 '%Y-%m-%d %H:%M:%S'))
    allow_share = db.Column(db.Boolean, default=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.user_name)

    @classmethod
    def login_check(cls, mail, password):
        user = cls.query.filter(db.and_(User.user_mail == mail, User.user_password == password)).first()
        if not user:
            return None
        return user


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upload_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    case_upload_time = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                        '%Y-%m-%d %H:%M:%S'))
    case_patient_name = db.Column(db.String(64), default="default")
    case_patient_gender = db.Column(db.String(64), default="default")
    case_patient_age = db.Column(db.String(64), default="default")
    case_photo_type = db.Column(db.String(64), default="default")
    case_photo_hash = db.Column(db.String(64), default="default")
    case_diagnose_type = db.Column(db.String(128), default="default")
    case_diagnose_result = db.Column(db.String(128), default="default")
    # case_ = db.Column(db.String(64))

    is_tagged = db.Column(db.Boolean, default=False)
    case_tag_info = db.Column(db.String(128), default="default")
    case_tag_time = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                     '%Y-%m-%d %H:%M:%S'))

    in_consultant = db.Column(db.Boolean, default=False)
    consultant_time = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                       '%Y-%m-%d %H:%M:%S'))
    consultation_message = db.Column(db.String(64), default="default")
    user = db.relationship(User, backref="cases")

    def __repr__(self):
        return '<Case %r>' % (self.case_patient_name)


class ExpertCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_case_id = db.Column(db.Integer, db.ForeignKey('case.id'), default=0)
    expert_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    expert_time = db.Column(db.DateTime, default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                   '%Y-%m-%d %H:%M:%S'))
    original_case = db.relationship(Case, backref="expertcases")
    expert = db.relationship(User, backref="expertcases")


#
# class Group(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     group_id = db.Column(db.ForeignKey(Group.id))
#     group = db.relationship(Group, backref='users')
#
# db.create_all()
# db.session.add(User(group=Group()))
# db.session.commit()
# u = User.query.get(1)
# print(u.group)


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_balance = db.Column(db.Integer, default=0)
    wallet_address = db.Column(db.String(64), default="default")


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), default=0)
    comment_content = db.Column(db.String(128), default="default")
    comment_time = db.Column(db.DateTime,
                             default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                       '%Y-%m-%d %H:%M:%S'))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    trans_from_address = db.Column(db.String(64), default="default")
    trans_to_address = db.Column(db.String(64), default="default")
    trans_amount = db.Column(db.Integer, default=0)
    trans_time = db.Column(db.DateTime,
                           default=datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    trans_typetype = db.Column(db.String(64), default="default")
    trans_spec = db.Column(db.String(64), default="default")
