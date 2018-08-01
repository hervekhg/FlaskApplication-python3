import os

class Config:
	SECRET_KEY = 'f334629b7e141f50f5edb664e038ccf4'
	DB_HOST = 'localhost'
	DB_USER = '237story'
	DB_PASSWORD = '237story!'
	DB_NAME = '237story'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' %(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
	#SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

	#MAIL_SERVER = 'smtp.googlemail.com'
	#MAIL_PORT = 587
	EMAIL_SENDER = 'contact@entreprendre.cm'
	MAIL_SERVER = 'localhost'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
		