from db import db
from flask_login import UserMixin

class DatingUser(db.Model, UserMixin):
    __tablename__ = 'dating_users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)  
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    search_gender = db.Column(db.String(10), nullable=False)
    about = db.Column(db.Text)
    is_hidden = db.Column(db.Boolean, default=False)
