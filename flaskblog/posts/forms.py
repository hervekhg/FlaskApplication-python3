from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	content = TextAreaField('Content',validators=[DataRequired()])
	submit = SubmitField('Post')

	def validate_title(self, title):
		if len(title.data) > 50:
			raise ValidationError('The title must be less than 50 Characters')

	def validate_content(self, content):
		if len(content.data) > 800:
			raise ValidationError('The content must be less than 800 Characters')