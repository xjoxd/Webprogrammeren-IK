import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from functools import wraps
from flask_session import Session

def upload_file(filename):
    db.execute("INSERT INTO images (path, id) VALUES (:path, :id)", path=filename, id=session["user_id"]





