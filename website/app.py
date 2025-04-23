from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from website.business import get_db  # Import the get_db function

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storeDB.db'  # database URI
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)

# Define the Business model
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100), nullable=False)


@app.route('/admin-dashboard')
def admin_dashboard():
    conn = get_db()  # Use the get_db function to connect to the database
    conn.row_factory = sqlite3.Row

    # Fetch businesses from the database
    businesses = conn.execute("SELECT BusinessID, Name, Owner FROM Business").fetchall()

    # Fetch drones from the database
    drones = conn.execute("SELECT DroneID, Name, Location FROM Drone").fetchall()

    # Fetch inventory from the database
    inventory = conn.execute("SELECT ProductID, Name, Stock FROM Product").fetchall()

    conn.close()
    return render_template("adminDashboard.html", businesses=businesses, drones=drones, inventory=inventory)
