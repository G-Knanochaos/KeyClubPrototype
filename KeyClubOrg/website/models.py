# database models stored here
from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # primary key is the main key for the user
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True)
    school = db.Column(db.String(100), server_default="")
