from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
  __tablename__ = "categories"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String, nullable = False)
  created_at = db.Column(db.DateTime, nullable = False)
  