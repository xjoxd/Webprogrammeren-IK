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

    # Als de gebruiker via GET de route bereikt heeft.
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

    # Als de gebruiker via GET de route bereikt heeft.
    else:
        return render_template("comment.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logt de gebruiker in."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # De gebruiker wordt hier ingelogd.
        log = model.login(username, password)

        # Excuses returnen als gebruikersnaam/wachtwoord fout is.
        if log == False:
            return apology("Invalid username or password.")

        # Gebruiker naar homepagina sturen.
        else:
            return redirect(url_for("homepage"))

    # Als de gebruiker via GET de route bereikt heeft.
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Logt de gebruiker uit."""

    # Alle gebruikers-id's vergeten.
    session.clear()

    # De gebruiker terugsturen naar de loginpagina.
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registreert de gebruiker."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":

        # Excuses returnen als de wachtwoorden niet hetzelfde zijn.
        if request.form.get("password") != request.form.get("confirm_password"):
            return apology("Passwords don't match.")

        # De gebruiker registreren.
        else:

            # Wachtwoord encrypten.
            password = request.form.get("password")
            hash = pwd_context.hash(password)

            # Ingevulde gebruikersnaam opvragen.
            username = request.form.get("username")

            # De gebruiker registreren en direct inloggen.
            reg = model.register(username, hash)

            # Checken of de gebruikersnaam niet reeds bestaat.
            if reg == "existing":
                return apology("Username already exists.")

            # De gebruiker naar de homepagina sturen.
            else:
                return redirect(url_for("homepage"))

    # Als de gebruiker via GET de route bereikt heeft.
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

    # Als de gebruiker via GET de route bereikt heeft.
    else:
        return render_template("post.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """De gebruiker kan tags toevoegen."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":

        # De tags worden aangevraagd en in de database opgeslagen.
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

        # Stuurt de gebruiker naar de homepagina.
        return render_template("settings.html")

    # Als de gebruiker via GET de route bereikt heeft.
    else:
        return render_template("settings.html")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Zoekt naar gebruikers met de gezochte tag."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":

        # Gezochte tag opvragen.
        session["tag"] = request.form.get("tag")

        # Gebruiker naar de discoverpagina doorsturen.
        return redirect(url_for("discover"))

    # Als de gebruiker via GET de route bereikt heeft.
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

    # Als de gebruiker via GET de route bereikt heeft.
    else:
        if profile == "empty":
            return apology("No more matches available.")
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

    # Als de gebruiker via GET de route bereikt heeft.
    else:
        return redirect(url_for("homepage"))


@app.route("/storegif", methods=["GET", "POST"])
@login_required
def storegif():
    """Slaat gifs op in de database."""

    # Als de gebruiker via POST kwam.
    if request.method == "POST":
        return redirect(url_for("post"))

    # Als de gebruiker via GET de route bereikt heeft.
    else:

        # URL van de gif opvragen.
        filename = request.args.get('url')

        # URL in de database zetten.
        model.giphy(filename)

        return redirect(url_for("post"))


@app.route("/getgif/<gifje>", methods=["GET"])
def getgif(gifje):
    """De gebruiker kan gifs zoeken."""

    return redirect("https://media1.giphy.com/media/" + gifje+"/giphy.gif")