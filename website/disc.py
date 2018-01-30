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
import random

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")

def disc(tag):
    """."""
    profiles = db.execute("SELECT id FROM users WHERE tag1=:tag1 OR tag2=:tag2 OR tag3=:tag3 OR tag4=:tag4 \
    OR tag5=:tag5 OR tag6=:tag6 OR tag7=:tag7 OR tag8=:tag8 OR tag9=:tag9 OR tag10=:tag10", \
    tag1=tag, tag2=tag, tag3=tag, tag4=tag, tag5=tag, tag6=tag, tag7=tag, tag8=tag, tag9=tag, tag10=tag)

    profiles_id = set(profile["id"] for profile in profiles)

    checked = db.execute("SELECT other_id FROM status WHERE id=:id", id=session["user_id"])
    checked_set = set(check["other_id"] for check in checked)

    show_profile = profiles_id - checked_set
    show_profiles = [id for id in show_profile if id != session["user_id"]]

    if show_profiles != []:
        return random.choice(show_profiles)
    else:
        return "empty"

def status_update(profile):
    return db.execute("INSERT INTO status (id, other_id) VALUES (:id, :other_id)", id=session["user_id"], other_id=profile)

def follow(profile):

    username = db.execute("SELECT username FROM users WHERE id=:followed_id", followed_id=profile)

    print(username)

    db.execute("INSERT INTO follow (follower_id, follower_username, followed_id, followed_username) \
    VALUES (:follower_id, :follower_username, :followed_id, :followed_username)",\
    follower_id=session["user_id"], follower_username=session["username"], followed_id=profile, followed_username=username[0]["username"])



def pics(profile):
    """Returnt foto's van de gebruiker."""

    pictures = db.execute("SELECT path FROM images WHERE id=:id ORDER BY timestamp DESC LIMIT 4", id=profile)
    return pictures

def usernamee(profile):
    """Returnt username."""

    username = db.execute("SELECT username FROM users WHERE id=:id", id=profile)
    return username[0]["username"]


















