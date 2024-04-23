# services/subscriptionService.py
from config.exts import db
from config.models import User
from sqlalchemy.exc import SQLAlchemyError

def get_subscription_service(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return {'subscription_level': user.subscription_level}
        else:
            return {'error': 'User not found'}, 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return {'error': str(e)}, 500
