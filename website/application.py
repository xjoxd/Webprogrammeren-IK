from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

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

    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # alle gebruiker id's vergeten
    session.clear()

    # als de gebruiker via POST kwam
    if request.method == "POST":

        # gebruikersnaam opvragen uit database
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # verzekeren dat gebruikersnaam bestaat en wachtwoord correct is
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # onthouden welke gebruiker ingelogd is
        session["user_id"] = rows[0]["id"]

        # stuur de gebruiker naar de homepagina
        return redirect(url_for("homepage"))

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

        # ervoor zorgen dat de wachtwoorden hetzelfde zijn
        if request.form.get("password") != request.form.get("confirm_password"):
            return apology("Passwords do not match!")

        # wachtwoord encrypten
        password = request.form.get("password")
        hash = pwd_context.hash(password)

        # checken of de gebruikersnaam niet reeds bestaat
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hash)
        if not result:
            return apology("Username already exists. Pick a different username.")

        # de gebruikersnaam ophalen uit de database
        rows = db.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))

        # onthouden welke gebruiker ingelogd is
        session["user_id"] = rows[0]["id"]

        # stuur de gebruiker naar de homepagina
        return redirect(url_for("homepage"))

    else:
        return render_template("register.html")

