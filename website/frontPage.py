from flask import Blueprint, render_template

frontPage = Blueprint('frontPage', __name__)

@frontPage.route('/')
def home():
    return render_template("frontPage.html")