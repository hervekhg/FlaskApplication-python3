import os

class Config:
	SECRET_KEY = 'f334629b7e141f50f5edb664e038ccf4'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	#MAIL_SERVER = 'smtp.googlemail.com'
	#MAIL_PORT = 587
	MAIL_SERVER = 'localhost'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
		