from flask import redirect, render_template, request, session
from functools import wraps

def reg():
    """Register user."""

    # als de gebruiker via POST kwam
    if request.method == "POST":

        # ervoor zorgen dat de wachtwoorden hetzelfde zijn
        if request.form.get("password") != request.form.get("confirm_password"):
            return apology("Passwords do not match!")

        # wachtwoord encrypten
        password = request.form.get("password")
        hash = pwd_context.hash(password)

        # checken of de gebruikersnaam niet reeds bestaat
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hash)
        if not result:
            return apology("Username already exists. Pick a different username.")

        # de gebruikersnaam ophalen uit de database
        rows = db.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))

        # onthouden welke gebruiker ingelogd is
        session["user_id"] = rows[0]["id"]

        # stuur de gebruiker naar de homepagina
        return redirect(url_for("homepage"))

    else:
        return render_template("register.html")

