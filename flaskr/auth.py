from flask import Blueprint, redirect, url_for, request, flash, session, abort
from flask_login import login_user, login_required, logout_user, current_user
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models import Users
import bcrypt

auth = Blueprint('auth', __name__)

from flask import Blueprint, render_template

@auth.route("/")
def landing():
    return render_template("base.html")

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
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
        else: # adding record in database
            # hash the password and encode it
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            new_user = Users(fname, lname, email, hashed)
            new_user.insert()

            session['email'] = email
            session["password"] = password

            return render_template("thanks.html", success=True)

@auth.route('/signin')
def signin_page():
    return render_template("signin.html")

@auth.route('/signin', methods=["POST"])
def signin():
    form = request.form

    email = form.get("email")
    password = form.get("password")
    user = Users.query.filter(Users.email == email).one()

    if not user:
        abort(404)
    if bcrypt.checkpw(password, user.password):
        login_user(user)
        return redirect(url_for("main.index"))
    else:
        flash("Invalid password")
        return render_template("signin.html")

@auth.route('/signout')
def signout():
    logout_user()
    return redirect(url_for("auth.signin_page"))