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

    # Voegt een like toe aan de database, als de foto geliked is.
    likes = db.execute("SELECT likes FROM images WHERE image_id=:image_id", image_id=image_id)
    likes = likes[0]["likes"] + 1
    db.execute("UPDATE images SET likes=:likes WHERE image_id=:image_id", likes=likes, image_id=image_id)

def commenting(image_id):
    """Voegt reacties oftewel comments toe aan de foto."""
    comments = db.execute
