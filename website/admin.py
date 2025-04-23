#Home page
import sqlite3
from website.business import get_db
from flask import Blueprint, render_template

# Create a Blueprint for admin routes
admin = Blueprint('admin', __name__)

@admin.route('/')
def admin_dashboard():

    conn = get_db()  # Use the get_db function to connect to the database
    conn.row_factory = sqlite3.Row

    users = conn.execute("""
        SELECT * FROM Users
            """).fetchall()

    # Fetch businesses from the database
    businesses = conn.execute("""
        SELECT Business.BusinessID, Business.BusinessName, Users.Name
        FROM Business
        JOIN BusinessOwner ON Business.BusinessID = BusinessOwner.BusinessID
        JOIN Users ON Users.UserID = BusinessOwner.UserID
            """).fetchall()
    
    inventory = conn.execute("""
    SELECT * FROM Product
        """).fetchall()

    drones = conn.execute("""
    SELECT * FROM Drone
        """).fetchall()

    # Fetch drones from the database
    #drones = conn.execute("SELECT DroneID, Name, Location FROM Drone").fetchall()

    # Fetch inventory from the database
    #inventory = conn.execute("SELECT ProductID, Name, Stock FROM Product").fetchall()

    conn.close()
    return render_template("adminDashboard.html", businesses = businesses, users = users, inventory = inventory, drones = drones)

