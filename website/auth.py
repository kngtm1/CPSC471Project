from flask import Blueprint, render_template, request, flash, session, redirect, url_for

auth = Blueprint('auth',__name__)

## login page under authentication
# Get: get url
# Post: send info to the server
@auth.route('/authenticate/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roles = request.form.get('role')  
        email = request.form.get('email')
        password = request.form.get('password')

        session['user_id'] = 1  # or however you're storing it (will need sql)
        session['role'] = roles  

        # Redirect based on role
        if roles == "customer":
            return redirect(url_for('customer.home'))
        elif roles == "businessOwner":
            return render_template("business_Home.html")
        elif roles == "admin":
            return render_template("adminDashboard.html")

    # This is the GET method - roles isn't accessed here!
    return render_template("login.html", boolean=True)

@auth.route('/authenticate/logout')
def logout():
    return render_template("frontPage.html")

@auth.route('/authenticate/signup', methods =['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        roles = request.form.get('role')#to differentiate between buyer and seller

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif not roles:
            flash('At least one role must be selected', category='error')
        else:
            #add user to database
            flash('Account created!', category='success')

            #INSERT INTO USER

        if roles == "customer":
            return render_template("login.html")
        elif roles == "businessOwner":
            return render_template("login.html")
        else:
            flash("Invalid role selected.", category='error')
            return render_template("signUp.html", boolean=True)
        
        
     # This is the GET method - roles isn't accessed here!
    return render_template("signUp.html", boolean=True)
        
