from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
from log import *
from reg import *
from upload import *
from homepage import *
#from settings import *
from disc import*


from flask_uploads import UploadSet, configure_uploads, IMAGES

# configure application
app = Flask(__name__)

photos = UploadSet("photos", IMAGES)

app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
configure_uploads(app, photos)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")


@app.route("/")
@login_required
def homepage():
    # if request.method == "POST":
    #     return redirect(url_for("homepage"))
    # else:
    #     return render_template("homepage.html")


    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():

    # als de gebruiker via POST kwam
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # gebruiker inloggen
        return log(username, password)

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # alle gebruiker id's vergeten
    session.clear()

    # gebruiker terugsturen naar de loginpagina
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # als de gebruiker via POST kwam
    if request.method == "POST":

        # excuses returenen als de wachtwoorden niet hetzelfde zijn
        if request.form.get("password") != request.form.get("confirm_password"):
            return apology("Passwords do not match!")

        # wachtwoord encrypten
        password = request.form.get("password")
        hash = pwd_context.hash(password)

        username = request.form.get("username")

        return reg(username, hash)

    else:
        return render_template("register.html")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST" and "photo" in request.files:

        filename = photos.save(request.files["photo"])

        return upload_file(filename)

    else:
        return render_template("post.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change password."""

    if request.method == "POST":

        # tag 1 aanvragen en in de database stoppen
        tag1 = request.form.get("tag1")
        tag1(tag1)

        # redirect user to home page
        return redirect(url_for("homepage"))

    else:
        return render_template("settings.html")

@app.route("/discover", methods=["GET", "POST"])
@login_required
def discover():
    if request.method == "POST":
        return disc()
    else:
        return render_template("discover.html")

