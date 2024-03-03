from flask import flash, render_template, request, redirect, url_for

from flask_login import login_user, current_user, logout_user, login_required

from project import app, db
from project.forms import RegistrationForm, LoginForm, UpdateProfileForm
from project.models import Students, Comments
from flask_login import UserMixin

from PIL import Image
import os
import secrets

@app.route("/")
def index():
	if current_user.is_authenticated:
		return redirect(url_for("user", username = current_user.first_name))
	return render_template("index.html")

@app.route("/registration", methods = ["GET", "POST"])
def registration():
	form = RegistrationForm()
	if current_user.is_authenticated:
		return redirect(url_for("user", username = current_user.first_name))
	print(form.errors)
	if form.validate_on_submit():
		first_name = form.first_name.data
		last_name = form.last_name.data
		birth_date = form.birth_date.data
		age = form.age.data
		gender = form.gender.data
		email = form.email.data
		phone = form.phone.data
		city = form.city.data
		country = form.country.data

		student = Students(first_name = first_name, last_name = last_name, birth_date = birth_date, age = age, gender = gender, email = email, phone = phone, city = city, country = country)
		db.session.add(student)
		db.session.commit()
		flash(f"Registration for {first_name} {last_name} is complete, please login", "success")
		return redirect(url_for("login"))
	return render_template("form.html", form = RegistrationForm())

@app.route("/login", methods = ["GET", "POST"])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		redirect(url_for("user", username = current_user.first_name))
	if form.validate_on_submit():
		first_name = form.first_name.data
		last_name = form.last_name.data
		email = form.email.data
		phone = form.phone.data
		user = Students.query.filter_by(
			first_name = first_name,
			last_name = last_name,
			email = email,
			phone = phone
			)
		if user:
			login_user(user, remember = True) 
			return redirect(url_for("user", username = current_user.first_name))
		flash('Login unsuccessful. Please check email and phone number', "danger")
	return render_template("login.html", form=LoginForm())

@app.route("/<username>")
@login_required
def user(username):
	if current_user.is_authenticated:
		return render_template("user.html", username = current_user.first_name)
	return redirect(url_for('login'))

@app.route("/profile_<username>")
@login_required
def profile(username):
	if current_user.is_authenticated:
		user = db.session.query(Students).filter_by(
			id = current_user.id
			).first()
		first_name = user.first_name
		last_name = user.last_name
		email = user.email
		phone = user.phone
		birth_date = user.birth_date
		age = user.age
		gender = user.gender
		city = user.city
		country = user.country
		image_file = url_for('static', filename = 'images/profiles/' + current_user.image_file)
		return render_template("profile.html", username = current_user.first_name, first_name = first_name, last_name = last_name, birth_date = birth_date, age = age, gender = gender, email = email, phone = phone, city = city, country = country, image_file = image_file)
	return redirect(url_for('index'))

def save_profile_picture(form_picture):
	random_file_name = secrets.token_hex(10)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_file_name = random_file_name + f_ext
	picture_file_path = os.path.join(app.root_path, 'static/images/profiles', picture_file_name)

	output_size = (125, 125)
	image = Image.open(form_picture)
	image.thumbnail(output_size)
	image.save(picture_file_path)

	print(picture_file_name)

	return picture_file_name

@app.route("/update_profile", methods=["GET", "POST"])
def update_profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		if form.image_file.data:
			current_user.image_file = save_profile_picture(form.image_file.data)
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.birth_date = form.birth_date.data
		current_user.age = form.age.data
		current_user.gender = form.gender.data
		current_user.email = form.email.data
		current_user.phone = form.phone.data
		current_user.city = form.city.data
		current_user.country = form.country.data
		db.session.commit()
		flash('Profile has been updated', 'success')
		return redirect(url_for('profile', username = current_user.first_name))
	return render_template('update.html', form = form, username = current_user.first_name)

@app.route("/logout")
def logout():
	# session.pop("username", None)
	logout_user()
	return redirect(url_for("index"))
