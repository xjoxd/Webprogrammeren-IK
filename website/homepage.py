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

def display():
    """Geeft foto's weer."""

    # Geeft de meest recentste foto's weer die opgehaald zijn vanuit de database.
    pictures = db.execute("SELECT * FROM images ORDER BY timestamp DESC")
    return pictures

def like(image_id):
    """Voegt een like toe aan de foto."""

    # Checken of de gebruiker niet al eens de foto geliked heeft.
    users = db.execute("SELECT id FROM likes WHERE image_id=:image_id AND id=:id", image_id=image_id, id=session["user_id"])

    if len(users) == 0:
        # Gebruiker die de foto geliked heeft in de database zetten.
        db.execute("INSERT INTO likes (image_id, id, username) VALUES (:image_id, :id, :username)", \
        image_id=image_id, id=session["user_id"], username=session["username"])

        # Zorgen dat de like counter één omhoog gaat.
        likes = db.execute("SELECT likes FROM images WHERE image_id=:image_id", image_id=image_id)
        likes = likes[0]["likes"] + 1
        db.execute("UPDATE images SET likes=:likes WHERE image_id=:image_id", likes=likes, image_id=image_id)

def commenting(image_id):
    """Voegt reacties oftewel comments toe aan de foto."""
    comments = db.execute
