from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_login import current_user
from flaskblog.models import Role


class RoleForm(FlaskForm):
	"""docstring for ClassName"""
	rolename = StringField('Rolename', 
						   validators=[DataRequired(),Length(min=2, max=20)])
	description = StringField('Description', 
						   validators=[DataRequired(),Length(min=2, max=100)])
	submit = SubmitField('Submit')

	def validate_rolename(self, rolename):
		if len(rolename.data) > 50:
			raise ValidationError('The title must be less than 50 Characters')

	def validate_description(self, description):
		if len(description.data) > 100:
			raise ValidationError('The description must be less than 100 Characters')