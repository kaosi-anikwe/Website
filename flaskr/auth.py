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
    req = request.form

    try:
        # getting form data
        fname = req.get("firstname")
        lname = req.get("lastname")
        email = req.get("email")
        password = req.get("password")
        account = req.get("account") if req.get("account") else "student"
        rpassword = req.get("repeatpassword")
        print(fname, lname, email, password, rpassword)
        if password != rpassword:
            flash("Password doesn't match")
            return redirect(url_for("auth.signup"))
        else:  # adding record in database
            # hash the password and encode it
            hashed = getHashed(password)

            new_user = Users(fname, lname, email, hashed, account)
            new_user.insert()

            return redirect(url_for("auth.login"))
    except:
        return redirect(url_for("auth.landing"))

@auth.route("/about")
def about():
    return render_template("about.html")

@auth.route("/contact")
def contact():
    return render_template("contact.html")
