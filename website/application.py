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





    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():
    return log()

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
####################################################################
    # # als de gebruiker via POST kwam
    # if request.method == "POST":
    #     if request.form.get("password") != request.form.get("confirm_password"):
    #         return apology("Passwords do not match!")

    #     # wachtwoord encrypten
    #     password = request.form.get("password")
    #     hash = pwd_context.hash(password)

    #     username = request.form.get("username")

    #     # checken of de gebruikersnaam niet reeds bestaat
    #     checken = check(username)
    #     if not checken:
    #         return apology("User already exists.")

    #     # de gebruiker registreren
    #     reg(username)

    #     # user id ophalen uit de database
    #     rows = rows(username)

    #     # onthouden welke gebruiker ingelogd is
    #     session["user_id"] = rows[0]["id"]

    #     # stuur de gebruiker naar de homepagina
    #     return redirect(url_for("homepage"))

    # else:
    #     return render_template("register.html")
################################################################

    return reg()

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST" and "photo" in request.files:
        filename = photos.save(request.files["photo"])
        ID = session["user_id"]
        username = usernames(ID)
        upload_file(filename, username)
        return redirect(url_for("homepage"))
    return render_template("post.html")
