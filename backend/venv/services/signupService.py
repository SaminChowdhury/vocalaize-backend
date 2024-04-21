# services/signupService.py
from config.exts import db
from sqlalchemy.exc import SQLAlchemyError
from config.models import User

def signupService(email, password):
    try:
        new_user = User(email=email, password=password)  # No subscription_level here
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except SQLAlchemyError as e:
        db.session.rollback()
        # Handle the exception, possibly logging it
        return None
