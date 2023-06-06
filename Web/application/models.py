from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer)
    filePath = db.Column(db.String)
    modelType = db.Column(db.String)
    dataType = db.Column(db.String)
    prediction = db.Column(db.Integer)
    predicted_on = db.Column(db.DateTime, nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer)
    modelType = db.Column(db.String)
    dataType = db.Column(db.String)
    imgs = db.Column(db.String)
    userScore = db.Column(db.Numeric(precision=10, scale=2))
    aiScore = db.Column(db.Numeric(precision=10, scale=2))
    quiz_on = db.Column(db.DateTime, nullable=False)
