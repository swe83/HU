from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from db.category import Category

db = SQLAlchemy()


class Place(db.Model):
    __tablename__ = "places"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer,
                            ForeignKey(Category.id),
                            nullable=False)
    description = db.Column(db.Text, nullable=False)
    street_address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String, nullable=False)
    image_file_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
  
    def __lt__(self, other):
        return self.name < other.name
