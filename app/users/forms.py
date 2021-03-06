from flask_wtf  import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):

	username = StringField('Username',validators=[DataRequired()])

	password = PasswordField('Password', validators=[DataRequired()])

	remember_me = BooleanField('Remember Me')

	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired()])

	email = StringField('Email', validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])

	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Register')

	def validate_username(self, username):

		user = User.query.filter_by(username=username.data).first()

		if user is not None:

			raise ValidationError('Please use a different username.')

	def validate_email(self, email):

		user = User.query.filter_by(email=email.data).first()

		if user is not None:

			raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired()])

	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])

	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

	submit = SubmitField('Submit')

	def __init__(self, original_username):

		super(EditProfileForm, self).__init__()

		self.original_username = original_username

	def validate_username(self, username):

		if username.data != self.original_username:

			user = User.query.filter_by(username=self.username.data).first()

			if user is not None:
				
				raise ValidationError('Please use a different username.')

class RequestResetForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired(), Email()])

	submit = SubmitField('Request Password Reset')


	def validate_email(self, email):

		user = User.query.filter_by(email=email.data).first()

		if user is None:

			raise ValidationError('There is no account with this email. You must register first.')


class ResetPasswordForm(FlaskForm):

	password = PasswordField('Password', validators=[DataRequired()])

	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Reset Password')