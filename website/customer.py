#Home page

from flask import Blueprint, render_template

customer = Blueprint('customer',__name__)

@customer.route('/customer', methods=['GET', 'POST'])
def home():
    return render_template("home.html")
