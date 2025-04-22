#Home page

from flask import Blueprint, render_template

# Create a Blueprint for admin routes
admin = Blueprint('admin', __name__)

@admin.route('/admin/')
def admin_dashboard():
    return render_template('adminDashboard.html')
