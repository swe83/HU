from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from db.category import Category
db = SQLAlchemy()

class Idea(db.Model):
  __tablename__ = "ideas"
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String, nullable = False)
  category_id = db.Column(db.Integer, ForeignKey(Category.id), nullable = False)
  description = db.Column(db.Text, nullable = False)
  skills = db.Column(db.String, nullable = False)
  zipcode = db.Column(db.String, nullable = False)
  first_name = db.Column(db.String, nullable = False)
  last_name = db.Column(db.String, nullable = False)
  email = db.Column(db.String, nullable = False)
  phone = db.Column(db.String)
  created_at = db.Column(db.DateTime, nullable = False)

  def __lt__(self, other):
    return self.title < other.title