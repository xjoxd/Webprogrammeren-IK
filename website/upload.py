from cs50 import SQL
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask import Flask, request, redirect, url_for
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from werkzeug.utils import secure_filename

import os

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")

def upload_file(filename, description):
    """Zet de foto's in de database."""

    # Selecteert de username vanuit de database.
    username = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])

    # Zet alleen de foto in de database en zet disctiption op None.
    if not description:
        photo = db.execute("INSERT INTO images (id, username, path, likes, description) \
        VALUES (:id, :username, :path, :likes, :description)", \
        id=session["user_id"], username=username[0]["username"], path=filename, likes=0, description=None)

    # Zet de foto en de description in de database.
    else:
        photo = db.execute("INSERT INTO images (id, username, path, likes, description) \
        VALUES (:id, :username, :path, :likes, :description)", \
        id=session["user_id"], username=username[0]["username"], path=filename, likes=0, description=description)

    return photo
