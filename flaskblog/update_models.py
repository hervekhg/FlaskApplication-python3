####################################
###
### Update database schema
###
###################################

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from flaskblog import db, login_manager
from flask import current_app
from flask_login import UserMixin
import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s' %('237story', '237story!', 'localhost', '237story')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20),nullable=False,default='default.png')
	password = db.Column(db.String(60),nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True, cascade="save-update, merge, delete")
	roles = db.relationship('Role', backref='authorrole', lazy=True)

	def __repr__(self):
		return "User('%s', '%s', '%s')" %s(self.username, self.email, self.image_file)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except Exception as e:
			return None
		return User.query.get(user_id)


class Post(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100), unique=True, nullable=False)
	slug = db.Column(db.String(100), unique=True, nullable=False)
	date_posted = db.Column(db.DateTime(),nullable=False, default=datetime.now)
	content = db.Column(db.Text(1000), nullable=False)
	like_post = db.Column(db.Integer, nullable=False)
	dislike_post = db.Column(db.Integer,nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return "Post('%s', '%s')" %s(self.title, self.date_posted)

class Role(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	rolename = db.Column(db.String(20), unique=True, nullable=False)
	description = db.Column(db.String(100), unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return "Role('%s', '%s')" %s(self.id, self.roles)

if __name__ == '__main__':
    manager.run()
