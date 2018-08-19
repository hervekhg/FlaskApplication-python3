from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	content = TextAreaField('Content',validators=[DataRequired()])
	submit = SubmitField('Post')

	def validate_title(self, title):
		if len(title.data) > 100:
			raise ValidationError('The title must be less than 50 Characters')

	def validate_content(self, content):
		if len(content.data) > 800 and len(content.data) < 150 :
			raise ValidationError('The content must be between 150 and 800 Characters')