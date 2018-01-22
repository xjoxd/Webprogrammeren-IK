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

def upload_file(filename, username):
    return db.execute("INSERT INTO images (id, username, path, likes) VALUES (:id, :username, :path, :likes)",\
    id=session["user_id"], username=username, path=filename, likes=0)





