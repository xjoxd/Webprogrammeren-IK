from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
from log import *
from reg import *
from upload import *

from flask_uploads import UploadSet, configure_uploads, IMAGES

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")


def disc(tag):

    profiles = db.execute("SELECT * FROM users WHERE tag1=:tag1 OR tag2=:tag2", tag1=tag, tag2=tag)

    for profile in profiles:
        images = db.execute("SELECT * FROM images WHERE id=:id ORDER BY timestamp DESC LIMIT 4", id=profile["id"])

    return images

def follow(images):
    db.execute("INSERT INTO follow (follower_id, follower_username, followed_id, followed_username \
    VALUES (:follower_id, :follower_username, :followed_id, :followed_username)",\
    follower_id=session["user_id"], follower_username=session["username"], )


