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


def reg(username, hash):
    check = db.execute("SELECT * FROM users WHERE username=:username", username=username)
    if len(check) > 0:
        return apology("User already exists.")

    # gebruiker registreren
    db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)

    # user id ophalen uit database
    rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)

    # onthouden welke gebruiker ingelogd is
    session["user_id"] = rows[0]["id"]


