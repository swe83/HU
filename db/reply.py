from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from db.user import User
from db.idea import Idea
db = SQLAlchemy()

class Reply (db.Model):
  __tablename__ = "replies"
  id = db.Column(db.Integer, primary_key = True)
  message = db.Column(db.Text, nullable = False)
  user_id = db.Column(db.Integer, ForeignKey(User.id), nullable = False)
  idea_id = db.Column(db.Integer, ForeignKey(Idea.id), nullable = False)
  created_at = db.Column(db.DateTime, nullable = False)