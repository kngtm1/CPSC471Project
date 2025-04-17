from flask import Blueprint, render_template, redirect, request, url_for
import sqlite3

business = Blueprint('business', __name__)
DB_PATH = "website/Data/StoreDB.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Display product list and form
@business.route('/')
def display():
    conn = get_db()
    products = conn.execute("SELECT * FROM Product").fetchall()
    conn.close()
    return render_template('business_Home.html', products=products, product=None)

# Load product into form for editing
@business.route('/edit/<int:productID>')
def editProduct(productID):
    conn = get_db()
    product = conn.execute("SELECT * FROM Product WHERE ProductID = ?", (productID,)).fetchone()
    products = conn.execute("SELECT * FROM Product").fetchall()
    conn.close()
    return render_template("business_Home.html", products=products, product=product)

# Add or update product
@business.route('/add', methods=['POST'])
def addProduct():
    productID = request.form.get('productID')
    name = request.form['name']
    category = request.form['category']
    price = request.form['price']
    stock = request.form['stock']

    conn = get_db()
    if productID:
        conn.execute("""
            UPDATE Product
            SET Name = ?, Category = ?, Price = ?, Stock = ?
            WHERE ProductID = ?
        """, (name, category, price, stock, productID))
        

    else:
        conn.execute("""
            INSERT INTO Product (Name, Category, Price, Stock)
            VALUES (?, ?, ?, ?)
        """, (name, category, price, stock))
    conn.commit()
    conn.close()
    return redirect(url_for('business.display'))

@business.route('/delete/<int:productID>')
def deleteProduct(productID):
    conn = get_db()
    conn.execute("DELETE FROM Product WHERE ProductID = ?", (productID,))
    conn.commit()
    conn.close()
    return redirect(url_for('business.display'))
