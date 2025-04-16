#Home page

from flask import Blueprint, render_template

admin = Blueprint('admin',__name__)

@admin.route('/admin', methods=['GET', 'POST'])
def home():
    return render_template("adminDashboard.html")
