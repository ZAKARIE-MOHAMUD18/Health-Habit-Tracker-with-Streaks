from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
class Habitlog(db.Model):
    __tablename__ = 'habitlogs'
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    note = db.Column(db.Text, nullable=True)


class Challange(db.Model):
    __tablename__ = 'challanges'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
  

class UserChallange(db.Model):
    __tablename__ = 'user_challanges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    challange_id = db.Column(db.Integer, db.ForeignKey('challanges.id'), nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    challange = db.relationship('Challange', backref=db.backref('user_challanges', lazy=True))