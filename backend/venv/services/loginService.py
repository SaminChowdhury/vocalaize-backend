import jwt
import datetime
from config.models import User
from config.exts import db
from werkzeug.security import check_password_hash
from sqlalchemy.exc import SQLAlchemyError

# Configuration for JWT
SECRET_KEY = "your_secret_key"  # This should be kept secret and secure
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30

def loginService(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # User is valid, create a JWT token
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=EXPIRATION_MINUTES),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            return token
        else:
            return False
    except SQLAlchemyError as e:
        db.session.rollback()
        # Handle the exception, possibly logging it
        return None
