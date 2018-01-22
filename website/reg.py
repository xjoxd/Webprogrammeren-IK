from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from flask import redirect, render_template, request, session
from functools import wraps
from helpers import *

# configure application
app = Flask(__name__)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")

def reg():
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
        check = db.execute(" SELECT * FROM users WHERE username=:username", username = request.form.get("username"))
        if check:
            return apology("user already exists")

        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hash)
        #if not result:
        #    return apology("Username already exists. Pick a different username.")

        # de gebruikersnaam ophalen uit de database
        rows = db.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))

        # onthouden welke gebruiker ingelogd is
        session["user_id"] = rows[0]["id"]

        # stuur de gebruiker naar de homepagina
        return redirect(url_for("homepage"))

    else:
        return render_template("register.html")