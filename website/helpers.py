import csv
import urllib.request

from cs50 import SQL
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask import redirect, render_template, request, session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")


def apology(message, code=400):
    """Stuurt een bericht als excuses naar de gebruiker."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Zorgt dat een gebruiker ingelogd moet zijn om functies te kunnen gebruiken.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def key():
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return key
