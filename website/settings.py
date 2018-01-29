from cs50 import SQL
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask import redirect, render_template, request, session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

# configure application
app = Flask(__name__)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")

def tag(first_tag, second_tag, third_tag, fourth_tag, fifth_tag, sixth_tag, seventh_tag, eigth_tag, ninth_tag, tenth_tag):
    """Zet de tags in de database."""

    if len(first_tag) > 0:

        # Stopt de tag in de database als er nog geen tag1 bestaat.
        if len(db.execute("SELECT tag1 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag1 = db.execute("INSERT INTO users (tag1) VALUES (:tag)", tag=first_tag)

        # Update de database als er al een tag1 bestaat.
        else:
            tag1 = db.execute("UPDATE users SET tag1=:tag WHERE id=:ID;", ID=session["user_id"], tag=first_tag)

    else:
        tag1 = db.execute("SELECT tag1 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(second_tag) > 0:

        # Stopt de tag in de database als er nog geen tag2 bestaat.
        if len(db.execute("SELECT tag2 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag2 = db.execute("INSERT INTO users (tag2) VALUES (:tag)", tag=second_tag)

        # Update de database als er al een tag2 bestaat.
        else:
            tag2 = db.execute("UPDATE users SET tag2=:tag WHERE id=:ID;", ID=session["user_id"], tag=second_tag)

    else:
        tag2 = db.execute("SELECT tag2 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(third_tag) > 0:

        # Stopt de tag in de database als er nog geen tag2 bestaat.
        if len(db.execute("SELECT tag3 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag3 = db.execute("INSERT INTO users (tag3) VALUES (:tag)", tag=third_tag)

        # Update de database als er al een tag2 bestaat.
        else:
            tag3 = db.execute("UPDATE users SET tag3=:tag WHERE id=:ID;", ID=session["user_id"], tag=third_tag)

    else:
        tag3 = db.execute("SELECT tag3 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(fourth_tag) > 0:

        # Stopt de tag in de database als er nog geen tag2 bestaat.
        if len(db.execute("SELECT tag4 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag4 = db.execute("INSERT INTO users (tag4) VALUES (:tag)", tag=fourth_tag)

        # Update de database als er al een tag2 bestaat.
        else:
            tag4 = db.execute("UPDATE users SET tag4=:tag WHERE id=:ID;", ID=session["user_id"], tag=fourth_tag)

    else:
        tag4 = db.execute("SELECT tag4 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(fifth_tag) > 0:

        # Stopt de tag in de database als er nog geen tag2 bestaat.
        if len(db.execute("SELECT tag5 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag5 = db.execute("INSERT INTO users (tag5) VALUES (:tag)", tag=fifth_tag)

        # Update de database als er al een tag2 bestaat.
        else:
            tag5 = db.execute("UPDATE users SET tag5=:tag WHERE id=:ID;", ID=session["user_id"], tag=fifth_tag)

    else:
        tag5 = db.execute("SELECT tag5 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(sixth_tag) > 0:

        # Stopt de tag in de database als er nog geen tag2 bestaat.
        if len(db.execute("SELECT tag6 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag6 = db.execute("INSERT INTO users (tag6) VALUES (:tag)", tag=sixth_tag)

        # Update de database als er al een tag2 bestaat.
        else:
            tag6 = db.execute("UPDATE users SET tag6=:tag WHERE id=:ID;", ID=session["user_id"], tag=sixth_tag)

    else:
        tag6 = db.execute("SELECT tag6 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(seventh_tag) > 0:

        # Stopt de tag in de database als er nog geen tag2 bestaat.
        if len(db.execute("SELECT tag7 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag7 = db.execute("INSERT INTO users (tag7) VALUES (:tag)", tag=seventh_tag)

        # Update de database als er al een tag2 bestaat.
        else:
            tag7 = db.execute("UPDATE users SET tag7=:tag WHERE id=:ID;", ID=session["user_id"], tag=seventh_tag)

    else:
        tag7 = db.execute("SELECT tag7 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(eigth_tag) > 0:

        # Stopt de tag in de database als er nog geen tag2 bestaat.
        if len(db.execute("SELECT tag8 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag8 = db.execute("INSERT INTO users (tag8) VALUES (:tag)", tag=eigth_tag)

        # Update de database als er al een tag2 bestaat.
        else:
            tag8 = db.execute("UPDATE users SET tag8=:tag WHERE id=:ID;", ID=session["user_id"], tag=eigth_tag)

    else:
        tag8 = db.execute("SELECT tag8 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(ninth_tag) > 0:

        # Stopt de tag in de database als er nog geen tag2 bestaat.
        if len(db.execute("SELECT tag9 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag9 = db.execute("INSERT INTO users (tag9) VALUES (:tag)", tag=ninth_tag)

        # Update de database als er al een tag2 bestaat.
        else:
            tag9 = db.execute("UPDATE users SET tag9=:tag WHERE id=:ID;", ID=session["user_id"], tag=ninth_tag)

    else:
        tag9 = db.execute("SELECT tag9 FROM users WHERE id=:ID", ID=session["user_id"])

    if len(tenth_tag) > 0:

        # Stopt de tag in de database als er nog geen tag1 bestaat.
        if len(db.execute("SELECT tag10 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            tag10 = db.execute("INSERT INTO users (tag10) VALUES (:tag)", tag=tenth_tag)

        # Update de database als er al een tag1 bestaat.
        else:
            tag10 = db.execute("UPDATE users SET tag10=:tag WHERE id=:ID;", ID=session["user_id"], tag=tenth_tag)

    else:
        tag10 = db.execute("SELECT tag10 FROM users WHERE id=:ID", ID=session["user_id"])


    return (tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9, tag10)

