from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
from log import *
from reg import *
from upload import *
from homepage import *
from settings import *
from disc import *

# configure application
app = Flask(__name__)

photos = UploadSet("photos", IMAGES)

app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
configure_uploads(app, photos)

# Zorgt ervoor dat de "responses" niet zijn gecached.
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

@app.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    """Geeft de homepagina weer."""

    if request.method == "POST":
        if request.form.get("like"):
            image_id = request.form.get("like")
            likes = like(image_id)
            pictures = display()
            return render_template("homepage.html", images=pictures, likes=likes)
        elif request.form.get("comment"):
            return redirect(url_for("comment"))
        else:
            pictures = display()
            return render_template("homepage.html", images=pictures)
    else:
        pictures = display()
        return render_template("homepage.html", images=pictures)

@app.route("/comment", methods=["GET", "POST"])
@login_required
def comment():
    # return apology("TODO")
    if request.method == "POST":
        if request.form.get("post"):
            if len(request.form.get("comment")) > 0:
                comment = request.form.get("comment")
                # image_id =
                # commenting(comment, image_id)
                pictures = display()
                return render_template("homepage.html", images=pictures)
            else:
                pictures = display()
                return render_template("homepage.html", images=pictures)
        elif request.form.get("cancel"):
            pictures = display()
            return render_template("homepage.html", images=pictures)

    else:
        return render_template("comment.html")


    #         likes = like(image_id)
    #         pictures = display()
    #         return render_template("homepage.html", images=pictures)
    #     else:
    #         pictures = display()
    #         return render_template("homepage.html", images=pictures)
    # else:
    #     pictures = display()
    #     return render_template("homepage.html", images=pictures)

@app.route("/login", methods=["GET", "POST"])
def login():
    """logt de gebruiker in."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # De gebruiker wordt hier ingelogd.
        log(username, password)

        # Stuurt de gebruiker naar de homepagina.
        return redirect(url_for("homepage"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Logt de gebruiker uit."""

    # Alle gebruikers hun id's vergeten.
    session.clear()

    # Stuurt de gebruiker terug naar de loginpagina.
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registreert de gebruiker."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":

        # Returned excuses als de wachtwoorden niet hetzelfde zijn.
        if request.form.get("password") != request.form.get("confirm_password"):
            return apology("Passwords do not match!")

        # Het wachtwoord encrypten.
        password = request.form.get("password")
        hash = pwd_context.hash(password)

        username = request.form.get("username")

        # De wordt geregistreerd met de functie reg.
        reg(username, hash)

        # Stuurt de gebruiker naar de homepagina.
        return redirect(url_for("homepage"))

    else:
        return render_template("register.html")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """De gebruiker kan een foto upoaden."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST" and "photo" in request.files:

        filename = photos.save(request.files["photo"])
        description = request.form.get("description")

        # De foto en de beschrijving wordt geüpload.
        upload_file(filename, description)

        # Stuurt de gebruiker naar de homepagina.
        return redirect(url_for("homepage"))

    else:
        return render_template("post.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """De gebruiker kan tags toevoegen."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":

        # De tags worden aangevraagd en in de database gestopt.
        first_tag = request.form.get("tag1")
        second_tag = request.form.get("tag2")

        # De tags worden aan de gebruiker gekoppeld.
        tag(first_tag, second_tag)

        # Stuurt de gebruiker naar de homepagina.
        return redirect(url_for("homepage"))

    else:
        return render_template("settings.html")

@app.route("/discover", methods=["GET", "POST"])
@login_required
def discover():
    if request.method == "POST":
        tag = request.form.get("tag")

        returns = disc(tag)

        for item in returns:
            user = item[1]
            images = item[0]

            return render_template("discover_profile.html", images=images)

            if request.form.get("like"):
                #follow()
                return render_template("discover_profile.html", images=images)

            elif request.form.get("dislike"):
                return render_template("discover_profile.html", images=images)

            else:
                return render_template("discover.html", images=images)

    else:
        return render_template("discover.html")



