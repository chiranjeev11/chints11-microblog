from flask_wtf  import FlaskForm, Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class EmptyForm(FlaskForm):

	submit = SubmitField('Submit')


class PostForm(FlaskForm):

	post = TextAreaField('Say Something', validators=[DataRequired(), Length(min=1, max=140)])

	submit = SubmitField('Submit')