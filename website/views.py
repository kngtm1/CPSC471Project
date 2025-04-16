#Home page
import sqlite3

from flask import Blueprint, render_template

views = Blueprint('views',__name__)

@views.route('/')
def home():
    #connecting to the sql
    connection = sqlite3.connect('website/Data/StoreDB.db')
    #connection.commit()
    reader = connection.cursor()
    
    #get products
    reader.execute("SELECT ProductID, Names, Description, RegistrationDate, Price FROM Product")
    products = reader.fetchall()
    
    #get orders
    reader.execute("SELECT OrderID, OrderDate, OrderTotal, Status FROM Orders")
    orders = reader.fetchall()
    
    #get order_item
    reader.execute("SELECT OrderID, Quantity FROM OrderItem")
    order_item = reader.fetchall()
    
    connection.close()
    #link to customer home page somehow?
    
    return render_template("home.html", products=products, orders=orders, order_item=order_item)
