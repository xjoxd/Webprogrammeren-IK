from cs50 import SQL
from flask import Flask, flash, redirect, render_template, jsonify, request, session, url_for
from flask_session import Session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
import model

import giphy_client
from giphy_client.rest import ApiException



# configure application
app = Flask(__name__)

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

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///website.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    """Geeft de homepagina weer."""

    if request.method == "POST":
        if request.form.get("comment"):
            session["image_id"] = request.form.get("comment")
            return redirect(url_for("comment"))
        else:
            pictures = model.display()
            get_comment = model.get_comments()
            return render_template("homepage.html", images=pictures, comments=get_comment)
    else:
        pictures = model.display()
        get_comment = model.get_comments()
        return render_template("homepage.html", images=pictures, comments=get_comment)

@app.route("/like", methods=["POST"])
def like():
    image_id = request.form.get("image_id")
    likes = model.like(image_id)
    return str(likes)

@app.route("/comment", methods=["GET", "POST"])
@login_required
def comment():
    # return apology("TODO")
    if request.method == "POST":
        if request.form.get("post"):
            if len(request.form.get("comment")) > 0:
                comment = request.form.get("comment")
                image_id = session.get("image_id")
                model.comment(comment, image_id)
                return redirect(url_for("homepage"))
            else:
                return redirect(url_for("homepage"))
        elif request.form.get("cancel"):
            return redirect(url_for("homepage"))
    else:
        return render_template("comment.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """logt de gebruiker in."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # De gebruiker wordt hier ingelogd.
        model.login(username, password)

        # Stuurt de gebruiker naar de homepagina.
        return redirect(url_for("homepage"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Logt de gebruiker uit."""

    # Alle gebruikers hun id's vergeten.
    session.clear()

    # Stuurt de gebruiker terug naar de loginpagina.
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registreert de gebruiker."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":

        # Returned excuses als de wachtwoorden niet hetzelfde zijn.
        if request.form.get("password") != request.form.get("confirm_password"):
            return apology("Passwords do not match!")

        # Het wachtwoord encrypten.
        password = request.form.get("password")
        hash = pwd_context.hash(password)

        username = request.form.get("username")

        # De wordt geregistreerd met de functie reg.
        model.register(username, hash)

        # Stuurt de gebruiker naar de homepagina.
        return redirect(url_for("homepage"))

    else:
        return render_template("register.html")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """De gebruiker kan een foto upoaden."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST" and "photo" in request.files:

        filename = photos.save(request.files["photo"])
        description = request.form.get("description")

        # De foto en de beschrijving wordt geüpload.
        model.upload_file(filename, description)

        # Stuurt de gebruiker naar de homepagina.
        return redirect(url_for("homepage"))

    else:
        return render_template("post.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """De gebruiker kan tags toevoegen."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":

        # De tags worden aangevraagd en in de database gestopt.
        first_tag = request.form.get("tag1")
        second_tag = request.form.get("tag2")
        third_tag = request.form.get("tag3")
        fourth_tag = request.form.get("tag4")
        fifth_tag = request.form.get("tag5")
        sixth_tag = request.form.get("tag6")
        seventh_tag = request.form.get("tag7")
        eigth_tag = request.form.get("tag8")
        ninth_tag = request.form.get("tag9")
        tenth_tag = request.form.get("tag10")

        # De tags worden aan de gebruiker gekoppeld.
        tags = model.tag(first_tag, second_tag, third_tag, fourth_tag, fifth_tag, sixth_tag, seventh_tag, \
        eigth_tag, ninth_tag, tenth_tag)
        print(tags)
        print(tags[0][0]["tag1"])

        # Stuurt de gebruiker naar de homepagina.
        return render_template("settings.html", tags=tags)

    else:
        return render_template("settings.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        session["tag"] = request.form.get("tag")
        return redirect(url_for("discover"))
    else:
        return render_template("discover.html")


@app.route("/discover", methods=["GET", "POST"])
@login_required
def discover():

    # Zoeken naar profielen met de door de gebruiker ingevulde tag.
    profile = model.discover(session["tag"])
    print(profile)

    if request.method == "POST":
        if request.form.get("like"):
            model.follow(profile)

        model.status_update(profile)

        return redirect(url_for("discover"))

    else:
        if profile == "empty":
            return apology("no more matches available")
        else:
            imges = model.pics(profile)
            username = model.username(profile)
            return render_template("discover_profile.html", pictures=imges, username=username)

@app.route("/gifsearch", methods=["GET", "POST"])
@login_required
def gifsearch():
    """De gebruiker kan gifs zoeken."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":

        gifsearch = request.form.get("searchgif")

        model.key()
        api_key = os.environ.get("API_KEY")

        # Geeft de API key mee.
        api_instance = giphy_client.DefaultApi()
        q = gifsearch
        limit = 15

        # Returned de gifs.
        try:
            api_response = api_instance.gifs_search_get(api_key, q, limit=limit)
            return render_template("gif.html", api_response=api_response)
        except ApiException as e:
            return apology ("No gifs selected")

    else:
        return redirect(url_for("homepage"))

@app.route("/storegif", methods=["GET", "POST"])
@login_required
def storegif():
    if request.method == "POST":
        return redirect(url_for("post"))
    else:
        filename = request.args.get('url')
        model.giphy(filename)
        return redirect(url_for("post"))

@app.route("/getgif/<gifje>", methods=["GET"])
def getgif(gifje):
    return redirect("https://media1.giphy.com/media/" + gifje+"/giphy.gif")
