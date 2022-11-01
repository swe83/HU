import os
from sqlalchemy import *

db_name = os.path.abspath("haven_for_unhoused.db")
engine = create_engine("sqlite:///"+db_name, echo = True)
metadata = MetaData()

users_table = Table(
  "users", metadata, 
  Column("id", Integer, primary_key = True),
  Column("username", String(20), nullable = False, unique = True),
  Column("password", String(20), nullable = False),
  Column("email", String(50)),
  Column("phone", String(20)),
  Column("first_name", String(50), nullable = False),
  Column("last_name", String(50), nullable = False),
  Column("created_at", DateTime, nullable = False, server_default = func.now())
)

categories_table = Table(
  "categories", metadata, 
  Column("id", Integer, primary_key = True),
  Column("name", String(20), nullable = False, unique = True),
  Column("created_at", DateTime, nullable = False, server_default = func.now())
)

places_table = Table(
  "places", metadata, 
  Column("id", Integer, primary_key = True),
  Column("name", String(50), nullable = False),
  Column("category_id", Integer, ForeignKey("categories.id"), nullable = False),
  Column("description", Text, nullable = False),
  Column("street_address", String(50), nullable = False),
  Column("city", String(50), nullable = False),
  Column("state", String(50), nullable = False),
  Column("zipcode", String(50), nullable = False),
  Column("email", String(50)),
  Column("phone", String(20)),
  Column("image_file_name", String(100), nullable = False),
  Column("created_at", DateTime, nullable = False, server_default = func.now())
)

ideas_table = Table(
  "ideas", metadata, 
  Column("id", Integer, primary_key = True),
  Column("title", String(50), nullable = False, unique = True),
  Column("category_id", Integer,  ForeignKey("categories.id"), nullable = False),
  Column("description", Text, nullable = False),
  Column("skills", String(100), nullable = False),
  Column("zipcode", String(50), nullable = False),
  Column("first_name", String(50), nullable = False),
  Column("last_name", String(50), nullable = False),
  Column("email", String(50), nullable = False),
  Column("phone", String(20)),
  Column("created_at", DateTime, nullable = False, server_default = func.now())
)

likes_table = Table(
  "likes", metadata,
  Column("id", Integer, primary_key = True),
  Column("user_id", Integer, ForeignKey("users.id"), nullable = False),
  Column("idea_id", Integer, ForeignKey("ideas.id"), nullable = False),
  Column("created_at", DateTime, nullable = False, server_default = func.now())
)

replies_table = Table(
  "replies", metadata,
  Column("id", Integer, primary_key = True),
  Column("message", Text, nullable = False),
  Column("user_id", Integer, ForeignKey("ideas.id"), nullable = False),
  Column("idea_id", Integer, ForeignKey("ideas.id"), nullable = False),
  Column("created_at", DateTime, nullable = False, server_default = func.now())
)

metadata.create_all(engine)

with engine.connect() as conn:

  sql = delete(categories_table)
  conn.execute(sql)
  categories_list = ["All", "Food", "Shelter", "Clothes", "Health", "Other"]
  for category_name in categories_list:
    sql = insert(categories_table).values(name = category_name)
    conn.execute(sql)

  sql = delete(places_table)
  conn.execute(sql)
  sql = insert(places_table).values(name = "CVS", category_id = 3, description = "xyz", street_address = " 3 x", city = "fremont", state = "CA", zipcode = "94539", image_file_name = "xyzabc")
  conn.execute(sql)
  sql = insert(places_table).values(name = "Walgreens", category_id = 4, description = "xyz", street_address = " 3 x", city = "fremont", state = "CA", zipcode = "94549", image_file_name = "xyzabc")
  conn.execute(sql)
  sql = insert(places_table).values(name = "Olive Garden", category_id = 1, description = "xyz", street_address = " 3 x", city = "fremont", state = "CA", zipcode = "94536", image_file_name = "xyzabc")
  conn.execute(sql)
  sql = insert(places_table).values(name = "Macys", category_id = 6, description = "xyz", street_address = " 3 x", city = "fremont", state = "CA", zipcode = "02108", image_file_name = "xyzabc")
  conn.execute(sql)