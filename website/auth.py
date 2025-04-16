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
    return render_template("home.html")

@auth.route('/signup', methods =['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        roles = request.form.getlist('role')#to differentiate between buyer and seller

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

            roles = request.form.getlist('role')#to differentiate between buyer and seller

            if 'buyer' in roles:
                if request.method == 'POST':#i dont actually know what this does, probably change it since i just copied it
                    dropoffLocation = request.form.get('dropoffLocation')
                    cursor.execute(
                        "INSERT INTO Customer (UserID, DropoffLocation) VALUES (?, ?)",
                        (user_id, 'TBD Dropoff') #havent touched user_id...
                    )

'''
            if 'seller' in roles:
                if request.method == 'POST':#i dont actually know what this does, probably change it since i just copied it
                    pickupLocation = request.form.get('pickupLocation')
                    cursor.execute(
                        "INSERT INTO BusinessOwner (UserID, PickupLocation) VALUES (?, ?)",
                        (user_id, 'TBD Pickup')  # replace 'TBD' with real pickup location
                    )

                conn.commit()
                conn.close()

                flash(f"Account created as {', '.join(roles)}!", category='success')
            except Exception as e:
                flash(f"Error creating account: {e}", category='error')
                '''

    return render_template("signUp.html")