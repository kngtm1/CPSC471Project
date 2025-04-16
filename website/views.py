#Home page
import sqlite3

from flask import Blueprint, render_template

views = Blueprint('views',__name__)

@views.route('/')
def home():
    connection = sqlite3.connect('website/Data/StoreDB.db')
    connection.commit()
    
    cursors = connection.cursor()
    cursors.execute("SELECT ProductID, Names, Description, RegistrationDate, Price FROM Product")
    products = cursors.fetchall()
    connection.close()
    #link to customer home page somehow?
    
    return render_template("home.html", products=products)
