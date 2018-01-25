from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from functools import wraps
from flask_session import Session

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")

def display():
    pictures = db.execute("SELECT * FROM images ORDER BY timestamp DESC")
    return pictures

def like(image_id):
    likes = db.execute("SELECT like FROM images WHERE image_id=:image_id", image_id=image_id)
    likes = cares[0]["like"] + 1
    like = db.execute("UPDATE like FROM images WHERE image_id=:image_id", image_id=likes)
    return like




