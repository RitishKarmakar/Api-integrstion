from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField, BooleanField 
from wtforms.validators import *
from flask_login import current_user
from app import app, User

class RegistrationForm(FlaskForm):
	username = StringField('User Name',validators = [DataRequired(), Length(min=2 , max= 20)])

	email = StringField('Email',validators=[DataRequired(),Email()])

	password = PasswordField('Password',validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')
	def validate_username(self,username):
		with app.app_context():

			user  = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('Validation Error please try another Username')
	def validate_email(self,email):
		with app.app_context():
			user  = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('Validation Error Please Try Another Email')
class LoginForm(FlaskForm):
	

	email = StringField('Email',validators=[DataRequired(), Email()])

	password = PasswordField('Password',validators = [DataRequired()])
	
	remember = BooleanField('Remember Me')

	submit = SubmitField('Sign In')

