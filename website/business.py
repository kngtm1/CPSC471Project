#Home page

from flask import Blueprint, render_template

business = Blueprint('business',__name__)

@business.route('/business', methods=['GET', 'POST'])
def home():
    return render_template("business_Home.html")
