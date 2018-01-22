from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
from log import *
from reg import *
<<<<<<< HEAD

=======
>>>>>>> ae8f68ed7c53bdbdc443bf4682526b5950db23c9

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
    return reg()
