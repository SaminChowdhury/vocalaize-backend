# services/validateTokenService.py
import jwt
from config.exts import db
from config.models import User
from sqlalchemy.exc import SQLAlchemyError

# Assuming the SECRET_KEY and ALGORITHM are defined as before
SECRET_KEY = "your_secret_key"  # This should be kept secret and secure
ALGORITHM = "HS256"

def validate_token_service(token):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload['user_id']

        # Fetch user details from the database
        user = User.query.get(user_id)
        if user:
            user_info = {
                'user_id': user.id,
                'email': user.email
            }
            return {'valid': True, 'user_info': user_info}
        return {'valid': False, 'error': 'User not found'}
    except jwt.ExpiredSignatureError:
        return {'valid': False, 'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'valid': False, 'error': 'Invalid token'}
    except SQLAlchemyError as e:
        return {'valid': False, 'error': str(e)}
