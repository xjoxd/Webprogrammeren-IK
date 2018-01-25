from cs50 import SQL
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

# configure application
app = Flask(__name__)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")

def log(username, password):
    """Logt gebruikers in en zet de gebruikers in de database."""

    # Gebruikersnaam wordt opgevraagd uit de database.
    rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)

    # Verzekert dat de gebruikersnaam bestaat en dat het wachtwoord correct is.
    if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
        return apology("invalid username and/or password")

    # Onthoud welke gebruiker ingelogd is.
    session["user_id"] = rows[0]["id"]
    session["username"] = rows[0]["username"]
