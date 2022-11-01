from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import *
import os
from os.path import exists
import bcrypt
from werkzeug.utils import secure_filename
import pgeocode

from db.user import User
from db.category import Category
from db.place import Place
from db.idea import Idea
from db.like import Like
from db.reply import Reply

app = Flask(__name__)

db_name = os.path.abspath("db/haven_for_unhoused.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

upload_folder = os.path.abspath("static")
app.config["UPLOAD_FOLDER"] = upload_folder


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        if session.get("username"):
            return redirect(url_for("index"))
        return render_template("registration.html")
    elif request.method == "POST":
        username_value = request.form["username"].strip().lower()
        password_value = request.form["password"]
        email_value = request.form["email"].strip()
        phone_value = request.form["phone"].strip()
        first_name_value = request.form["first_name"].strip()
        last_name_value = request.form["last_name"].strip()

        bytes = password_value.encode("utf-8")
        salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(bytes, salt)

        #check if username is taken
        sql = select(User).where(User.username == username_value)
        user_found = db.session.scalars(sql).first()
        if user_found:
            return render_template("registration.html",
                                   error="Username is already taken")

        user = User(username=username_value,
                    password=encrypted_password,
                    email=email_value,
                    phone=phone_value,
                    first_name=first_name_value,
                    last_name=last_name_value,
                    created_at=func.now())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("username"):
            return redirect(url_for("index"))
        return render_template("login.html")
    elif request.method == "POST":
        username_value = request.form["username"].strip().lower()
        password_value = request.form["password"]

        bytes = password_value.encode("utf-8")
        salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(bytes, salt)

        user = db.session.query(User).filter(
            User.username == username_value).first()
        if user == None:
            return render_template("login.html",
                                   error="Invalid Username or Password")
        correct_password = bcrypt.checkpw(bytes, user.password)
        if not correct_password:
            return render_template("login.html",
                                   error="Invalid Username or Password")
        session["username"] = user.username
        session["user_id"] = user.id
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session["username"] = None
    session["user_id"] = None
    return redirect(url_for("login"))


@app.route("/search", methods=["GET", "POST"])
def search():
    sql = select(Category)
    categories = []
    for category in db.session.scalars(sql):
        categories.append(category)
    if request.method == "GET":
        return render_template("search.html", categories=categories)
    elif request.method == "POST":
        category_id = request.form["category"]
        zipcode = request.form["zipcode"]
        try:
            zipcodenum = int(zipcode)
            results = []
            sql = select(Place).where(Place.category_id == category_id)
            if category_id == "1":
                sql = select(Place)
            distcalc = pgeocode.GeoDistance("US")
            for place in db.session.scalars(sql):
                distance = distcalc.query_postal_code(zipcode, place.zipcode)
                sql_category = select(Category).where(
                    Category.id == place.category_id)
                category = db.session.scalars(sql_category).first()
                category_name = category.name
                results.append((distance, place.name, place, category_name))
            sorted_results = sorted(results)
            return render_template("search.html",
                                   categories=categories,
                                   results=sorted_results[0:5], category_id = int(category_id), zipcode = zipcode)
        except Exception as e:
            return render_template("search.html",
                                   categories=categories,
                                   error="invalid zipcode " + str(e))


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not session.get("username"):
        return render_template("upload.html", login_required=True)

    sql = select(Category)
    categories = []
    for category in db.session.scalars(sql):
        categories.append(category)
        
    if request.method == "GET":
        
        return render_template("upload.html", categories=categories)
    elif request.method == "POST":

        place_name_value = request.form["place_name"].strip()
        category_id_value = request.form["category_id"]
        description_value = request.form["description"].strip()
        street_address_value = request.form["street_address"].strip()
        city_value = request.form["city"].strip()
        state_value = request.form["state"].strip()
        zip_code_value = request.form["zip_code"].strip()
        email_value = request.form["email"].strip()
        if email_value == '':
          email_value = "N/A"
        phone_value = request.form["phone"].strip()
        file = request.files["image_file_name"]
        filename = file.filename
        if "." not in filename:
            return render_template("upload.html", error="Invalid File")
        file_extension = filename.rsplit(".", 1)[1].lower()
        if file_extension not in ["png", "jpg", "jpeg", "gif"]:
            return render_template("upload.html", error="Invalid File")
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        #make sure file name is unique

        file.save(file_path)

        place = Place(name=place_name_value,
                      category_id=category_id_value,
                      description=description_value,
                      street_address=street_address_value,
                      city=city_value,
                      state=state_value,
                      zipcode=zip_code_value,
                      email=email_value,
                      phone=phone_value,
                      image_file_name=filename,
                      created_at=func.now())

        db.session.add(place)
        db.session.commit()
        return render_template(
            "upload.html",
            success="Your place has been added to our database!", categories=categories)


@app.route("/submit_ideas", methods=["GET", "POST"])
def submit_ideas():
    if not session.get("username"):
        return render_template("submit_ideas.html", login_required=True)
    sql = select(Category)
    categories = []
    for category in db.session.scalars(sql):
        categories.append(category)

    if request.method == "GET":
        return render_template("submit_ideas.html", categories=categories)
    elif request.method == "POST":

        title_value = request.form["title"].strip()
        category_id_value = request.form["category_id"]
        description_value = request.form["description"].strip()
        skills_value = request.form["skills"].strip()
        zip_code_value = request.form["zip_code"].strip()
        first_name_value = request.form["first_name"].strip()
        last_name_value = request.form["last_name"].strip()
        email_value = request.form["email"].strip()
        phone_value = request.form["phone"].strip()

        idea = Idea(title=title_value,
                    category_id=category_id_value,
                    description=description_value,
                    skills=skills_value,
                    zipcode=zip_code_value,
                    first_name=first_name_value,
                    last_name=last_name_value,
                    email=email_value,
                    phone=phone_value,
                    created_at=func.now())
        db.session.add(idea)
        db.session.commit()

        return render_template(
            "submit_ideas.html",
            categories=categories,
            success="Your idea has been added to our database!")


@app.route("/ideas", methods=["GET", "POST"])
def ideas():
    if request.method == "GET":
        sql = select(Idea)
        ideas = []
        for idea in db.session.scalars(sql):
            sql_replies = select(Reply).where(Reply.idea_id == idea.id)
            replies = []
            for reply in db.session.scalars(sql_replies):
                replies.append(reply)
            user_liked = False
            like_count = 0
            sql_likes = select(Like).where(Like.idea_id == idea.id)
            for like in db.session.scalars(sql_likes):
                like_count += 1
                if like.user_id == session.get("user_id"):
                    user_liked = True
            ideas.append((like_count, idea, replies, user_liked))
        sorted_ideas = sorted(ideas, reverse=True)
        return render_template("ideas.html", ideas=sorted_ideas)
    elif request.method == "POST":
        return render_template("ideas.html")


@app.route("/reply", methods=["POST"])
def reply():
    if not session.get("username") or not session.get("user_id"):
        return redirect(url_for("login"))
    reply_text_value = request.form["reply_text"].strip()
    idea_id_value = request.form["idea_id"]
    reply = Reply(message=reply_text_value,
                  user_id=session.get("user_id"),
                  idea_id=idea_id_value,
                  created_at=func.now())
    db.session.add(reply)
    db.session.commit()
    return redirect(url_for("ideas"))


@app.route("/like", methods=["POST"])
def like():
    if not session.get("username") or not session.get("user_id"):
        return redirect(url_for("login"))
    idea_id_value = request.form["idea_id"]
    like = Like(user_id=session.get("user_id"),
                idea_id=idea_id_value,
                created_at=func.now())
    db.session.add(like)
    db.session.commit()
    return redirect(url_for("ideas"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/resources")
def resources():
    return render_template("resources.html")


app.run(host='0.0.0.0', port=81)