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

def tag1(tag):
    # tag in de database stoppen als er nog geen tag1 bestaat
    if len(db.execute("SELECT tag1 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
        db.execute("INSERT INTO users (tag1) VALUES (:tag)", tag=tag)
    # database updaten als er al een tag1 bestaat
    else:
        db.execute("UPDATE users SET tag1=:tag WHERE id=:ID;", ID=session["user_id"], tag=tag)

    return redirect(url_for("homepage"))




