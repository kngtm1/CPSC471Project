#Customer page
import sqlite3
import threading
import time

from flask import Blueprint, render_template
from flask import request, redirect, url_for, session, jsonify

#Defining Flask blueprint for customer, tells Flask where to find things
customer = Blueprint('customer',__name__)

#Customer homepage
@customer.route('/customer', methods=['GET', 'POST'])
def home():
    #connecting to the sql
    connection = sqlite3.connect('website/Data/StoreDB.db')
    connection.row_factory = sqlite3.Row    #Access via columns
    user_id = session.get('user_id')    #user_ID to log in
    reader = connection.cursor()
    
    #get products
    reader.execute("SELECT ProductID, Name, Description, Price, Stock FROM Product")
    products = reader.fetchall()
    
    # get orders
    reader.execute("SELECT OrderID, OrderDate, OrderTotal, Status FROM Orders")
    orders = reader.fetchall()
  
    
    # Find if the logged-in users order is in 'Processing' status
    reader.execute("SELECT OrderID FROM Orders WHERE UserID = ? AND Status = 'Processing'", (user_id,))
    order_row = reader.fetchone()

    #Default empty cart, price, and order status
    order_items = [] 
    total_price = 0
    order_status = None

    if order_row:
        order_id = order_row["OrderID"]

        #Fetch items
        reader.execute("""
            SELECT P.Name AS Name, P.Price, OI.Quantity, OI.ProductID
            FROM OrderItem OI
            JOIN Product P ON OI.ProductID = P.ProductID
            WHERE OI.OrderID = ?
        """, (order_id,))
        order_items = reader.fetchall()
        
        #Calculating total price for the cart
        total_price = sum(item["Price"] * item["Quantity"] for item in order_items)
        
        #Getting the order status, which should be 'Processing'
        reader.execute("SELECT Status FROM Orders WHERE OrderID = ?", (order_id,))
        status_row = reader.fetchone()
        order_status = status_row["Status"] if status_row else None
    
    connection.close()
    
    #return all the information and bring it to home.html
    return render_template("home.html", products=products, orders=orders, order_items=order_items, total_price=total_price, order_status=order_status)


from flask import request, redirect, url_for, session

#Add to Order
@customer.route('/add_to_order', methods=['POST'])
def add_to_order():
    #getting required information
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')
    user_id = session.get('user_id')  # assuming this is set during login

    connection = sqlite3.connect('website/Data/StoreDB.db')
    cursor = connection.cursor()

    #Check if a 'Proccessing' order already exists
    cursor.execute("SELECT OrderID FROM Orders WHERE UserID = ? AND Status = 'Processing'", (user_id,))
    result = cursor.fetchone()

    if result:
        order_id = result[0]
        #checks if there is already an open 'Proccessing' order
        cursor.execute("UPDATE Orders SET Status = 'Processing' WHERE OrderID = ?", (order_id,))
        connection.commit()
    else:
        # Create new order if none exists
        cursor.execute("INSERT INTO Orders (OrderDate, OrderTotal, AdminID, UserID, Status) VALUES (date('now'), 0, 2, ?, 'Processing')", (user_id,))
        order_id = cursor.lastrowid

    #Check if the item is already in the cart (OrderItem)
    cursor.execute("SELECT Quantity FROM OrderItem WHERE OrderID = ? AND ProductID = ?", (order_id, product_id))
    existing = cursor.fetchone()

    if existing:
        # If it exists, update the quantity
        new_quantity = existing[0] + int(quantity)
        cursor.execute("""
            UPDATE OrderItem
            SET Quantity = ?
            WHERE OrderID = ? AND ProductID = ?
        """, (new_quantity, order_id, product_id))
    else:
        # Otherwise, insert a new item
        cursor.execute("""
            INSERT INTO OrderItem (OrderID, ProductID, Quantity)
            VALUES (?, ?, ?)
        """, (order_id, product_id, quantity))
    
    connection.commit()
    connection.close()

    #redirect so we dont get duplicates
    return redirect(url_for('customer.home'))


#Remove from Order
@customer.route('/remove_from_order', methods=['POST'])
def remove_from_order():
    product_id = request.form.get('product_id')
    user_id = session.get('user_id')

    connection = sqlite3.connect('website/Data/StoreDB.db')
    cursor = connection.cursor()

    # Find current processing order
    cursor.execute("SELECT OrderID FROM Orders WHERE UserID = ? AND Status = 'Processing'", (user_id,))
    result = cursor.fetchone()

    if result:
        order_id = result[0]
        # Remove the product from OrderItem
        cursor.execute("DELETE FROM OrderItem WHERE OrderID = ? AND ProductID = ?", (order_id, product_id))

    connection.commit()
    connection.close()

    return redirect(url_for('customer.home'))

#Checkout
@customer.route('/checkout', methods=['POST'])
def checkout():
    #Handle frontend JSON request format
    if request.headers.get("Content-Type") == "application/json":
        request.get_json(silent=True)
    user_id = session.get('user_id')

    connection = sqlite3.connect('website/Data/StoreDB.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Get the processing order
    cursor.execute("SELECT OrderID FROM Orders WHERE UserID = ? AND Status = 'Processing'", (user_id,))
    result = cursor.fetchone()

    if result:
        order_id = result[0]
        
        #set to Processing before transition timer
        cursor.execute("UPDATE Orders SET Status = 'Processing' WHERE OrderID = ?", (order_id,))
        connection.commit()
        
        #Sending timer
        def mark_as_sending_then_delivered(order_id):
            time.sleep(5)  # wait before sending
            delayed_conn = sqlite3.connect('website/Data/StoreDB.db')
            delayed_cursor = delayed_conn.cursor()
            delayed_cursor.execute("UPDATE Orders SET Status = 'Sending' WHERE OrderID = ?", (order_id,))
            delayed_conn.commit()
    
            time.sleep(5)  # wait before delivery
            delayed_cursor.execute("UPDATE Orders SET Status = 'Delivered' WHERE OrderID = ?", (order_id,))
            delayed_conn.commit()
            delayed_conn.close()

        #Starting background thread
        threading.Thread(target=mark_as_sending_then_delivered, args=(order_id,)).start()
        connection.commit()
        
        #Fetch products in the order
        cursor.execute("SELECT ProductID, Quantity FROM OrderItem WHERE OrderID = ?", (order_id,))
        items = cursor.fetchall()
        
        #Update stock levels
        for item in items:
            cursor.execute("UPDATE Product SET Stock = Stock - ? WHERE ProductID = ?", (item["Quantity"], item["ProductID"]))
        connection.commit()

        #clear cart after checkout
        cursor.execute("DELETE FROM OrderItem WHERE OrderID = ?", (order_id,))
        connection.commit()

        connection.close()
        return jsonify({"order_id": order_id})  # Send the order ID to the frontend for status display

    connection.close()
    return jsonify({"error": "No active order"}), 400
