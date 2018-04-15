from app import db
from datetime import datetime
ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True)
	password = db.Column(db.String(64))
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	about_me = db.Column(db.String(140))
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
		return '<User %r>' % (self.username)

	@classmethod
	def login_check(cls, username, password):
		user = cls.query.filter(db.and_(User.username == username, User.password == password)).first()
		if not user:
			return None
		return user
