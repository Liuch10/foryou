from app import db
from datetime import datetime
ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_name = db.Column(db.String(64), unique = True)
	user_password = db.Column(db.String(64))
	user_type = db.Column(db.String(64))
    user_city = db.Column(db.String(64))
    user_hospital = db.Column(db.String(64))
    user_department = db.Column(db.String(64))
    user_phone = db.Column(db.String(64))
    user_chain_address = db.Column(db.String(64))
    user_reg_time = db.Column(db.DateTime)
	last_seen = db.Column(db.DateTime)

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
	def login_check(cls, username, password):
		user = cls.query.filter(db.and_(User.user_name == username, User.user_password == password)).first()
		if not user:
			return None
		return user

class Case(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	upload_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	case_chain_address = db.Column(db.String(64))
	case_info = db.Column(db.String(64))
	is_diagnosed = db.Column(db.Integer, default = 0)
    diagnosis_info = db.Column(db.String(128))
    in_consultant = db.Column(db.Integer, default = 0)
    consultation_message = db.Column(db.String(64))

	def __repr__(self):
		return '<Case %r>' % (self.body)

class Wallet(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	wallet_balance = db.Column(db.Integer)
	wallet_address = db.Column(db.String(64))

class Consultation(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	comment_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
	comment_content = db.Column(db.String(128))
	comment_time = db.Column(db.DateTime, 
		default = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
    
class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	trans_from_address = db.Column(db.String(64))
	trans_to_address = db.Column(db.String(64))
	trans_amout = db.Column(db.Integer)
	trans_time = db.Column(db.DateTime, 
		default = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
	trans_typetype = db.Column(db.String(64))
