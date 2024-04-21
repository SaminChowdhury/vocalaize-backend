# services/loginService.py

from config.models import User
from config.exts import db
from werkzeug.security import check_password_hash
from sqlalchemy.exc import SQLAlchemyError

def loginService(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # You would also generate a token or session here
            # For demonstration purposes, let's just return True
            return True
        else:
            return False
    except SQLAlchemyError as e:
        db.session.rollback()
        # Handle the exception, possibly logging it
        return None
