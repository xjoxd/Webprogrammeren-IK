from cs50 import SQL
from functools import wraps
from flask import Flask, flash, redirect, render_template, jsonify, request, session, url_for
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
import random

import giphy_client
from giphy_client.rest import ApiException

# Applicatie configureren.
app = Flask(__name__)

# Foto upload mechanisme initialiseren.
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
configure_uploads(app, photos)

# Zorgt ervoor dat de "responses" niet zijn gecached.
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Session configureren om het bestandensysteem te gebruiken.
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# CS50 Library configureren om SQLite database te gebruiken.
db = SQL("sqlite:///website.db")


def display():
    """Geeft foto's weer."""

    # Uit de database halen wie door de gebruiker gevolgd worden.
    picture_info = db.execute("SELECT follow.followed_id, images.* FROM follow INNER JOIN images \
    ON follow.followed_id=images.id WHERE follow.follower_id=:follower_id ORDER BY images.timestamp DESC",\
    follower_id=session["user_id"])

    return picture_info

def get_comments():
    """Haalt de comments op."""

    # Comments in chronologische volgorde uit de database halen.
    get_comment = db.execute("SELECT * FROM comments ORDER BY timestamp DESC")

    return get_comment

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

        return likes

    else:

        # Hetzelfde aantal likes returnen als de foto al eens door de gebruiker geliked is.
        likes = db.execute("SELECT likes FROM images WHERE image_id=:image_id", image_id=image_id)

        return likes[0]["likes"]

def comment(comment, image_id):
    """Voegt reacties oftewel comments toe aan de foto."""

    # Comments worden opgevraagd uit de database.
    comments = db.execute("INSERT INTO comments (image_id, comment, id, username) VALUES (:image_id, :comment, :id, :username)", \
    image_id=image_id, comment=comment, id=session["user_id"], username=session["username"])

    return comments

def login(username, password):
    """Logt gebruikers in en zet de gebruikers in de database."""

    # Gebruikersnaam wordt opgevraagd uit de database.
    rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)

    # Verzekert dat de gebruikersnaam bestaat en dat het wachtwoord correct is.
    if len(rows) != 1 or not pwd_context.verify(password, rows[0]["hash"]):
        return False
    else:
        # Onthoud welke gebruiker ingelogd is.
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

def register(username, hash):
    """Registeert gebruikers en zet de gebruikers in de database."""

    # Checken of de gebruikersnaam al bestaat.
    check = db.execute("SELECT * FROM users WHERE username=:username", username=username)
    if len(check) > 0:
        return "existing"

    # Zet de gebruikers in de database.
    db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)

    # Haalt de user id op uit database.
    rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)

    # Onthoudt welke gebruiker ingelogd is.
    session["user_id"] = rows[0]["id"]
    session["username"] = rows[0]["username"]

    # Zorgt ervoor dat de gebruiker zichzelf volgt.
    db.execute("INSERT INTO follow (follower_id, follower_username, followed_id, followed_username) \
    VALUES (:follower_id, :follower_username, :followed_id, :followed_username)",\
    follower_id=session["user_id"], follower_username=session["username"], \
    followed_id=session["user_id"], followed_username=session["username"])

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

def giphy(filename):
    """Zet de gifs in de database."""

    # Selecteert de username vanuit de database.
    username = db.execute("SELECT username FROM users WHERE id=:id", id=session["user_id"])

    # Zet alleen de foto in de database en zet disctiption op None.
    gif = db.execute("INSERT INTO images (id, username, path, likes, description) \
    VALUES (:id, :username, :path, :likes, :description)", \
    id=session["user_id"], username=username[0]["username"], path=filename, likes=0, description=None)

    return gif

def discover(tag):
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

    db.execute("INSERT INTO follow (follower_id, follower_username, followed_id, followed_username) \
    VALUES (:follower_id, :follower_username, :followed_id, :followed_username)",\
    follower_id=session["user_id"], follower_username=session["username"], followed_id=profile, \
    followed_username=username[0]["username"])

def pics(profile):
    """Returnt foto's van de gebruiker."""

    pictures = db.execute("SELECT path FROM images WHERE id=:id ORDER BY timestamp DESC LIMIT 4", id=profile)
    return pictures

def username(profile):
    """Returnt username."""

    username = db.execute("SELECT username FROM users WHERE id=:id", id=profile)
    return username[0]["username"]

def tag(first_tag, second_tag, third_tag, fourth_tag, fifth_tag, sixth_tag, seventh_tag, eigth_tag, ninth_tag, tenth_tag):
    """Zet de tags in de database."""

    if len(first_tag) > 0:

        # Stopt de tag in de database als er nog geen tag1 bestaat.
        if len(db.execute("SELECT tag1 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag1) VALUES (:tag)", tag=first_tag)

        # Update de database als er al een tag1 bestaat.
        else:
            db.execute("UPDATE users SET tag1=:tag WHERE id=:ID;", ID=session["user_id"], tag=first_tag)

    if len(second_tag) > 0:

        if len(db.execute("SELECT tag2 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag2) VALUES (:tag)", tag=second_tag)

        else:
            db.execute("UPDATE users SET tag2=:tag WHERE id=:ID;", ID=session["user_id"], tag=second_tag)

    if len(third_tag) > 0:

        if len(db.execute("SELECT tag3 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag3) VALUES (:tag)", tag=third_tag)

        else:
            db.execute("UPDATE users SET tag3=:tag WHERE id=:ID;", ID=session["user_id"], tag=third_tag)

    if len(fourth_tag) > 0:

        if len(db.execute("SELECT tag4 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag4) VALUES (:tag)", tag=fourth_tag)

        else:
            db.execute("UPDATE users SET tag4=:tag WHERE id=:ID;", ID=session["user_id"], tag=fourth_tag)

    if len(fifth_tag) > 0:

        if len(db.execute("SELECT tag5 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag5) VALUES (:tag)", tag=fifth_tag)

        else:
            db.execute("UPDATE users SET tag5=:tag WHERE id=:ID;", ID=session["user_id"], tag=fifth_tag)

    if len(sixth_tag) > 0:

        if len(db.execute("SELECT tag6 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag6) VALUES (:tag)", tag=sixth_tag)

        else:
            db.execute("UPDATE users SET tag6=:tag WHERE id=:ID;", ID=session["user_id"], tag=sixth_tag)

    if len(seventh_tag) > 0:

        if len(db.execute("SELECT tag7 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag7) VALUES (:tag)", tag=seventh_tag)

        else:
            db.execute("UPDATE users SET tag7=:tag WHERE id=:ID;", ID=session["user_id"], tag=seventh_tag)

    if len(eigth_tag) > 0:

        if len(db.execute("SELECT tag8 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag8) VALUES (:tag)", tag=eigth_tag)

        else:
            db.execute("UPDATE users SET tag8=:tag WHERE id=:ID;", ID=session["user_id"], tag=eigth_tag)

    if len(ninth_tag) > 0:

        if len(db.execute("SELECT tag9 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag9) VALUES (:tag)", tag=ninth_tag)

        else:
            db.execute("UPDATE users SET tag9=:tag WHERE id=:ID;", ID=session["user_id"], tag=ninth_tag)

    if len(tenth_tag) > 0:

        if len(db.execute("SELECT tag10 FROM users WHERE id=:ID", ID=session["user_id"])) == 0:
            db.execute("INSERT INTO users (tag10) VALUES (:tag)", tag=tenth_tag)

        else:
            db.execute("UPDATE users SET tag10=:tag WHERE id=:ID;", ID=session["user_id"], tag=tenth_tag)

def key():
    """Geeft de API-key."""

    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return key
