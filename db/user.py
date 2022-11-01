from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
db = SQLAlchemy()

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String, nullable = False)
  password = db.Column(db.String, nullable = False)
  email = db.Column(db.String)
  phone = db.Column(db.String)
  first_name = db.Column(db.String, nullable = False)
  last_name = db.Column(db.String, nullable = False)
  created_at = db.Column(db.DateTime, nullable = False)
  