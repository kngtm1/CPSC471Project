from . import db
from flask_login import UserMixin

class User(db.model, UserMixin):
    id = db.Column()
