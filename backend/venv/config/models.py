# models.py

from config.exts import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    subscription_level = db.Column(db.String(50), nullable=True)  # Allow null if not specified

    def __init__(self, email, password, subscription_level=None):
        self.email = email
        self.password = password
        self.subscription_level = subscription_level
