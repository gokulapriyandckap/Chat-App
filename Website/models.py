from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    userName = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone = True), default = func.now())
    messages = db.relationship('messages_table')

class messages_table (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    message_text = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime(timezone = True), default = func.now())

