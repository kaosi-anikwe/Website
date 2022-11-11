from flask import Blueprint, redirect, url_for, request, flash, session, abort, render_template
from flask_login import login_user, login_required, logout_user, current_user
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models import Users
import bcrypt
import hashlib

auth = Blueprint("auth", __name__)

def getHashed(text):  # function to get hashed email/password as it is reapeatedly used
    salt = "ITSASECRET"  # salt for password security
    hashed = text + salt  # salt for password security, a random string will be added to password and hashed together below
    hashed = hashlib.md5(hashed.encode())  # encrypting with md5 hash, best for generating passwords for db
    hashed = hashed.hexdigest()  # converting to string
    return hashed  # gives hashed text back

@auth.route("/")
def landing():
    return render_template("base.html")


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def signin():
    form = request.form

    email = form.get("email")
    password = form.get("password")
    user = Users.query.filter(Users.email == email).one_or_none()

    if not user:
        flash("User not found")
        return render_template("login.html")
    if getHashed(password) == user.password:
        login_user(user)
        return redirect(url_for("main.index"))
    else:
        flash("Invalid password")
        return render_template("login.html")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_page():
    # if method post in index
    # if "email" in session:
    #     return redirect(url_for("logged_in"))
    req = request.form
    print(req)
    # Validating Empty Fields
    missing = list()
    # Getting Immutable Multi Dict Data
    for k, v in req.items():
        if v == "":
            missing.append(k)

    if missing:
        comment = f"Missing field: {',  '.join(missing)}".title()
        return render_template("thanks.html", comment=comment, miss=True)
    else:
        # getting form data
        fname = req.get("firstname")
        lname = req.get("lastname")
        email = req.get("email")
        password = req.get("password")
        rpassword = req.get("repeatpassword")
        print(fname, lname, email, password, rpassword)
        if password != rpassword:
            comment = "Password doesn't match"
            return render_template("thanks.html", comment=comment, miss=True)
        else:  # adding record in database
            # hash the password and encode it
            hashed = getHashed(password)
            # hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            new_user = Users(fname, lname, email, hashed)
            new_user.insert()

            session["email"] = email
            session["password"] = password

            return render_template("thanks.html", success=True)
