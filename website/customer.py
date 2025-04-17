#Home page
import sqlite3

from flask import Blueprint, render_template

customer = Blueprint('customer',__name__)

@customer.route('/customer', methods=['GET', 'POST'])
def home():
    #connecting to the sql
    connection = sqlite3.connect('website/Data/StoreDB.db')
    connection.row_factory = sqlite3.Row
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
    
    return render_template("home.html", products=products, orders=orders, order_item=order_item)


from flask import request, redirect, url_for, session

@customer.route('/add_to_order', methods=['POST'])
def add_to_order():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')
    user_id = session.get('user_id')  # assuming this is set during login

    connection = sqlite3.connect('website/Data/StoreDB.db')
    cursor = connection.cursor()

    # Step 1: Check if the user has an open Order
    cursor.execute("SELECT OrderID FROM Orders WHERE UserID = ? AND Status = 'Processing'", (user_id,))
    result = cursor.fetchone()

    if result:
        order_id = result[0]
    else:
        # Create new order if none exists
        cursor.execute("INSERT INTO Orders (OrderDate, OrderTotal, AdminID, UserID, Status) VALUES (date('now'), 0, 2, ?, 'Processing')", (user_id,))
        order_id = cursor.lastrowid

    # Step 2: Add the item to OrderItem
    cursor.execute("INSERT INTO OrderItem (OrderID, ProductID, Quantity) VALUES (?, ?, ?)", (order_id, product_id, quantity))

    connection.commit()
    connection.close()

    return redirect(url_for('customer.home'))
