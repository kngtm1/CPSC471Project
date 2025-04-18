from flask import Blueprint, render_template, request, flash, session, redirect, url_for
import sqlite3
auth = Blueprint('auth',__name__)

## login page under authentication
# Get: get url
# Post: send info to the server
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # 'Customer', 'Business', or 'Admin'

        user = None

        cursor = sqlite3.connect("website/Data/StoreDB.db")
        cursor.row_factory = sqlite3.Row
        cursor = cursor.cursor()

        print("hit")

        

        if role == 'customer':
            user = cursor.execute("""
                SELECT Users.UserID, Users.Name
                FROM Users
                JOIN Customer ON Users.UserID = Customer.UserID
                WHERE Users.Email = ? AND Users.Password = ?
            """, (email, password)).fetchone()
            print("customer")


        elif role == 'businessOwner':
            print("hit")

            user = cursor.execute("""
                SELECT Users.UserID, Users.Name, BusinessOwner.BusinessID 
                FROM Users
                JOIN BusinessOwner ON Users.UserID = BusinessOwner.UserID
                WHERE Users.Email = ? AND Users.Password = ?
            """, (email, password)).fetchone()

        elif role == 'admin':
            user = cursor.execute("""
                SELECT Users.UserID, Users.Name, Admin.AdminID 
                FROM Users
                JOIN Admin ON Users.UserID = Admin.UserID
                WHERE Users.Email = ? AND Users.Password = ?
            """, (email, password)).fetchone()

        if user:
            session['user_id'] = user["UserID"]
            session['role'] = role

            if role == 'Business':
                session['business_id'] = user['BusinessID']
            elif role == 'Admin':
                session['admin_id'] = user['AdminID']

            flash('Login successful!', 'success')

            cursor.close()

            # Redirect to respective dashboards
            if role == 'customer':
                return redirect(url_for('customer.home'))
            elif role == 'businessOwner':
                return redirect(url_for('business.display'))
            elif role == 'admin':
                return redirect(url_for('admin.dashboard'))

        else:
            flash('Invalid credentials or role mismatch.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    return render_template("frontPage.html")

@auth.route('/signup', methods =['GET', 'POST'])
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
        
