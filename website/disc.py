from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
from log import *
from reg import *
from upload import *

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")

def disc(tag):
    """."""

    profiles = db.execute("SELECT * FROM users WHERE tag1=:tag1 OR tag2=:tag2 OR tag3=:tag3 OR tag4=:tag4 \
    OR tag5=:tag5 OR tag6=:tag6 OR tag7=:tag7 OR tag8=:tag8 OR tag9=:tag9 OR tag10=:tag10 \
    ", tag1=tag, tag2=tag, tag3=tag, tag4=tag, tag5=tag, tag6=tag, tag7=tag, tag8=tag, tag9=tag, tag10=tag)

    # Returned excuses als er geen profielen met de gezogde tags zijn.
    if not profiles:
        return apology("There are no users with this tag")

    poss = []

    for profile in profiles:
        # Geeft 4 foto's weer van een profiel met de gezochte tekst.
        images = db.execute("SELECT path FROM images WHERE id=:id ORDER BY timestamp DESC LIMIT 4", id=profile["id"])
        if images:
            poss.append([images,profile["username"], profile["id"]])

    return(poss)

def follow(followed_id):

    username = db.execute("SELECT username FROM users WHERE id=:followed_id", followed_id = followed_id)

    print(followed_id)
    print(username)

    match = db.execute("INSERT INTO follow (follower_id, follower_username, followed_id, followed_username \
    VALUES (:follower_id, :follower_username, :followed_id, :followed_username)",\
    follower_id=session["user_id"], follower_username=session["username"], followed_id=followed_id, followed_username=username)

    return match