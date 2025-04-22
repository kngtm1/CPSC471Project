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
            cursor.execute("SELECT * FROM Admin WHERE Email = ? AND Password = ?", (email, password))
            user = cursor.fetchone()
            if user:
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin.admin_dashboard'))  # Ensure this route exists

        if user:
            session['user_id'] = user["UserID"]
            session['role'] = role

            if role == 'businessOwner':
                conn = sqlite3.connect("website/Data/StoreDB.db")
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()

                cur.execute("SELECT BusinessID FROM BusinessOwner WHERE UserID = ?", (session['user_id'],))
                result = cur.fetchone()

                if result:
                    print("hit business")
                    session['business_id'] = result['BusinessID']
                else:
                    print("did not hit business")
                    session['business_id'] = None  # or handle it however you want

                cur.close()
                conn.close()

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

        if not email or len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
            return render_template("signUp.html")

        elif not firstName or len(firstName) < 2:
            flash('First name must be greater than 2 characters', category='error')
            return render_template("signUp.html")

        elif not password1 or password1 != password2:
            flash('Passwords don\'t match', category='error')
            return render_template("signUp.html")
        elif not roles:
            flash('At least one role must be selected', category='error')
            return render_template("signUp.html")
        else:
            #add user to database
            flash('Account created!', category='success')

        conn = sqlite3.connect("website/Data/StoreDB.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            # Insert user
            cur.execute("""
                INSERT INTO Users (Name, Email, PhoneNumber, Password)
                VALUES (?, ?, ?, ?)
            """, (firstName, email, 1234567890, password1))  # Replace dummy phone # as needed
            user_id = cur.lastrowid

            if roles == "customer":
                cur.execute("""
                    INSERT INTO Customer (UserID, DropoffLocation)
                    VALUES (?, ?)
                """, (user_id, "Default Dropoff"))  # You can replace with form value

            elif roles == "businessOwner":
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('auth.businessRegistration', user_id=user_id))

            conn.commit()
            flash("Account created successfully!", category='success')

        except sqlite3.IntegrityError as e:
            flash("Error: Email already exists or invalid data.", category='danger')
            print(e)
            conn.rollback()
            return render_template("signUp.html")


        if roles == "customer":
            return redirect(url_for('auth.login'))
        elif roles == "businessOwner":
            return redirect(url_for('auth.businessRegistration', user_id=user_id))
        else:
            flash("Invalid role selected.", category='error')
            return render_template("signUp.html")
        
        
     # This is the GET method - roles isn't accessed here!
    return render_template("signUp.html")

@auth.route('/businessRegistration', methods=['GET', 'POST'])
def businessRegistration():
    user_id = request.args.get('user_id') if request.method == 'GET' else request.form.get('user_id')

    if request.method == 'POST':
        businessName = request.form.get('businessName')
        category = request.form.get('category')
        description = request.form.get('description')

        conn = sqlite3.connect("website/Data/StoreDB.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Business (BusinessName, Description, Category)
            VALUES (?, ?, ?)
        """, (businessName, description, category))
        business_id = cur.lastrowid

        cur.execute("""
            INSERT INTO BusinessOwner (UserID, PickupLocation, AdminID, BusinessID)
            VALUES (?, ?, ?, ?)
        """, (user_id, "Default Pickup", 1, business_id))

        conn.commit()
        cur.close()
        conn.close()
        flash("Business registration complete. You can now log in.", "success")

        session['user_id'] = user_id
        session['business_id'] = business_id
        session['role'] = 'businessOwner'

        return redirect(url_for('auth.login'))

    return render_template("businessRegistration.html", user_id=user_id)



