from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    api_key = db.Column(db.String(200), unique=True) 
    requests_made = db.Column(db.Integer, default=0)
   

from datetime import datetime

class URLHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    url = db.Column(db.String(500))
    result = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)