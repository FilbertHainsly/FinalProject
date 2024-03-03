from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, DateField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, NumberRange, ValidationError

from project.models import Students

from flask_login import current_user


class RegistrationForm(FlaskForm):
	first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=10)])
	last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=10)])
	birth_date = DateField("Birth Date", validators=[DataRequired()])
	age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=10, max=100)])
	gender = RadioField("Gender", choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired(), Email()])
	phone = StringField("Phone Number", validators=[DataRequired()])
	city = StringField("City", validators=[DataRequired()])
	country = StringField("Country", validators=[DataRequired()])
	submit = SubmitField("Register")

	def validate_email(self, email):
		student = Students.query.filter_by(email = email.data).first()
		if student:
			raise ValidationError('Email has been taken')

class LoginForm(FlaskForm):
	first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=10)])
	last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=10)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	phone = StringField("Phone Number", validators=[DataRequired()])
	submit = SubmitField("Login")

class UpdateProfileForm(FlaskForm):
	first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=10)])
	last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=10)])
	birth_date = DateField("Birth Date", validators=[DataRequired()])
	age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=10, max=100)])
	gender = RadioField("Gender", choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired(), Email()])
	phone = StringField("Phone Number", validators=[DataRequired()])
	city = StringField("City", validators=[DataRequired()])
	country = StringField("Country", validators=[DataRequired()])
	
	image_file = FileField("Profile Picture", validators = [FileAllowed(['jpg', 'jpeg', 'png'])])

	submit = SubmitField("Update")

	def validate_email(self, email):
		student = Students.query.filter_by(email = email.data).first()
		if student:
			raise ValidationError('Email has been taken')