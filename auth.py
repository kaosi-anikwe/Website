from flask import Blueprint, redirect, url_for, request, flash, session
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

auth = Blueprint('auth', __name__)

from flask import Blueprint, render_template

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup_page():
    req = request.form
    print(req)
    # if method post in index
    # if "email" in session:
    #     return redirect(url_for("logged_in"))
    if request.method == "POST":
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
                print("Password doesn't match")
            else:
                # adding record in database
                record = User(firstname=fname, lastname=lname, email=email, password=password)
                db.session.add(record)
                db.session.commit()
                session['email'] = email
                session["password"] = password
                return render_template("thanks.html", success=True)

        #     # hash the password and encode it
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    else:
        return render_template("signup.html")