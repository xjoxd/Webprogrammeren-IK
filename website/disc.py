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


def disc():

    # ervoor zorgen dat de wachtwoorden hetzelfde zijn
    tag = request.form.get("tag")

    randoms = db.execute(" SELECT * FROM users WHERE tag=:tag", tag=tag)

        #while randoms:
        #   profile():
        #
        #   if like:
        #       follow
        #
        #   profile = old
        #
        #   rerun

    return render_template("discover.html")

#def profile(randoms):
