from flask import Blueprint, render_template

auth = Blueprint('auth',__name__)

## login page under authentication
@auth.route('/login')
def login():
    return render_template("login.html", boolean = True)
## passes text to to login.html


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/signup')
def signup():
    return render_template("signUp.html")