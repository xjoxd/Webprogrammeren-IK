from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
# configure application
app = Flask(__name__)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")
def log():

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