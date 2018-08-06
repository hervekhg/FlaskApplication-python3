import os

class Config:
	SECRET_KEY = 'f334629b7e141f50f5edb664e038ccf4'
	DB_HOST = os.environ.get('DB_HOST')
	DB_USER = os.environ.get('DB_USER')
	DB_PASSWORD = os.environ.get('DB_PASSWORD')
	DB_NAME = os.environ.get('DB_NAME')
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' %(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
	#SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	EMAIL_SENDER = 'contact@entreprendre.cm'
	#MAIL_SERVER = 'localhost'
	#MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
		