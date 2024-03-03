from flask_login import UserMixin

from project import db, login_manager

from datetime import datetime

@login_manager.user_loader
def load_student(id):
	return Students.query.get(id)

class Students(db.Model, UserMixin):
	id = db.Column(db.Integer, db.Identity(start = 1, cycle=True) ,primary_key = True)
	first_name = db.Column(db.String(20), nullable = False)
	last_name = db.Column(db.String(20), nullable = False)
	birth_date = db.Column(db.String(20), nullable = False)
	age = db.Column(db.Integer, nullable = False)
	gender = db.Column(db.String(20), nullable = False)
	email = db.Column(db.String(50), unique = True, nullable = False)
	phone = db.Column(db.String(20), unique = True, nullable = False)
	city = db.Column(db.String(20), nullable = False)
	country = db.Column(db.String(20), nullable = False)
	image_file = db.Column(db.String(100), unique = False, nullable = False, default = "default.jpg")

	comments = db.relationship('Comments', backref = 'creator', lazy = True)

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text, nullable = False)
	image_content = db.Column(db.Text, nullable = False, default = "None")
	commenter_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable = False)