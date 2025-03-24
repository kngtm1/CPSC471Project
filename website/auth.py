from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth',__name__)

## login page under authentication
# Get: get url
# Post: send info to the server
@auth.route('/login', methods =['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", boolean = True)



@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/signup', methods =['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        else:
            #add user to database
            flash('Account created!', category='success')

    return render_template("signUp.html")