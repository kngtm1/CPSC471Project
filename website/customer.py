#Customer page
import sqlite3
import threading
import time

from flask import Blueprint, render_template

customer = Blueprint('customer',__name__)

@customer.route('/customer', methods=['GET', 'POST'])
def home():
    #connecting to the sql
    connection = sqlite3.connect('website/Data/StoreDB.db')
    connection.row_factory = sqlite3.Row
    user_id = session.get('user_id')
    #connection.commit()
    reader = connection.cursor()
    
    #get products
    reader.execute("SELECT ProductID, Names, Description, RegistrationDate, Price FROM Product")
    products = reader.fetchall()
    
    # get orders
    reader.execute("SELECT OrderID, OrderDate, OrderTotal, Status FROM Orders")
    orders = reader.fetchall()

    # get order_item
    reader.execute("SELECT OrderID, Quantity FROM OrderItem")
    order_item = reader.fetchall()    
    
    # Find the logged-in user's processing order
    reader.execute("SELECT OrderID FROM Orders WHERE UserID = ? AND Status = 'Processing'", (user_id,))
    order_row = reader.fetchone()

    order_items = []
    total_price = 0
    order_status = None

    if order_row:
        order_id = order_row["OrderID"]

        reader.execute("""
            SELECT P.Names, P.Price, OI.Quantity, OI.ProductID
            FROM OrderItem OI
            JOIN Product P ON OI.ProductID = P.ProductID
            WHERE OI.OrderID = ?
        """, (order_id,))
        order_items = reader.fetchall()
    
        total_price = sum(item["Price"] * item["Quantity"] for item in order_items)
        
        
        reader.execute("SELECT Status FROM Orders WHERE OrderID = ?", (order_id,))
        status_row = reader.fetchone()
        order_status = status_row["Status"] if status_row else None
    
    connection.close()
    
    return render_template("home.html", products=products, orders=orders, order_items=order_items, total_price=total_price, order_status=order_status)


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

    # Step 2: Check if the item already exists in OrderItem
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
        # Otherwise, insert a new record
        cursor.execute("""
            INSERT INTO OrderItem (OrderID, ProductID, Quantity)
            VALUES (?, ?, ?)
        """, (order_id, product_id, quantity))
    
    connection.commit()
    connection.close()

    return redirect(url_for('customer.home'))

@customer.route('/remove_from_order', methods=['POST'])
def remove_from_order():
    product_id = request.form.get('product_id')
    user_id = session.get('user_id')

    connection = sqlite3.connect('website/Data/StoreDB.db')
    cursor = connection.cursor()

    # Find the processing order
    cursor.execute("SELECT OrderID FROM Orders WHERE UserID = ? AND Status = 'Processing'", (user_id,))
    result = cursor.fetchone()

    if result:
        order_id = result[0]
        # Remove the product from OrderItem
        cursor.execute("DELETE FROM OrderItem WHERE OrderID = ? AND ProductID = ?", (order_id, product_id))

    connection.commit()
    connection.close()

    return redirect(url_for('customer.home'))

@customer.route('/checkout', methods=['POST'])
def checkout():
    user_id = session.get('user_id')

    connection = sqlite3.connect('website/Data/StoreDB.db')
    cursor = connection.cursor()

    # Get the processing order
    cursor.execute("SELECT OrderID FROM Orders WHERE UserID = ? AND Status = 'Processing'", (user_id,))
    result = cursor.fetchone()

    if result:
        order_id = result[0]
        cursor.execute("UPDATE Orders SET Status = 'Sending' WHERE OrderID = ?", (order_id,))
        connection.commit()

        def mark_as_delivered_later(order_id):
            time.sleep(5)
            delayed_conn = sqlite3.connect('website/Data/StoreDB.db')
            delayed_cursor = delayed_conn.cursor()
            delayed_cursor.execute("UPDATE Orders SET Status = 'Delivered' WHERE OrderID = ?", (order_id,))
            delayed_conn.commit()
            delayed_conn.close()

        threading.Thread(target=mark_as_delivered_later, args=(order_id,)).start()

    connection.close()
    return redirect(url_for('customer.home'))