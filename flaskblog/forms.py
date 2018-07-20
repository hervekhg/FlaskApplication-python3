from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User 

class RegistrationForm(FlaskForm):
	"""docstring for ClassName"""
	username = StringField('Username', 
						   validators=[DataRequired(),Length(min=2, max=20)])

	email = StringField('Email', 
						validators=[DataRequired(),Email()])

	password = PasswordField('Password', validators=[DataRequired()])

	confirm_password = PasswordField('Confirm Password', 
		                             validators=[DataRequired(), EqualTo('password')])		

	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is already taken. Please choose another')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is already taken. Please choose another')

class LoginForm(FlaskForm):
	"""docstring for ClassName"""

	email = StringField('Email', 
						validators=[DataRequired(),Email()])

	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	"""docstring for ClassName"""
	username = StringField('Username', 
						   validators=[DataRequired(),Length(min=2, max=20)])

	email = StringField('Email', 
						validators=[DataRequired(),Email()])

	picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])])

	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is already taken. Please choose another')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is already taken. Please choose another')


class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	content = TextAreaField('Content',validators=[DataRequired()])
	submit = SubmitField('Post')

	def validate_title(self, title):
		if len(title.data) > 50:
			raise ValidationError('The title must be less than 50 Characters')

	def validate_content(self, content):
		if len(content.data) > 500:
			raise ValidationError('The content must be less than 500 Characters')

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(),Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('That email is not exist on our system. You must register first')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])

	confirm_password = PasswordField('Confirm Password', 
		                             validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

