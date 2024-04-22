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
# models.py


class AudioTranslation(db.Model):
    __tablename__ = 'audio_translations'
    
    translation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    input_drive_path = db.Column(db.String(255), nullable=False)
    output_drive_path = db.Column(db.String(255), nullable=True)  # Assuming this might be set later
    source_language = db.Column(db.String(50), nullable=False)
    target_language = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())

