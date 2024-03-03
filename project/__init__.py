from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "3479734e3f074eda09645c61ab00a8f0"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from project import routes