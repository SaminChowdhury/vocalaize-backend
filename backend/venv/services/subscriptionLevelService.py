# services/subscriptionService.py

from config.exts import db
from config.models import User
from sqlalchemy.exc import SQLAlchemyError

def selectSubscriptionService(user_id, subscription_level):
    try:
        user = User.query.get(user_id)
        if user:
            user.subscription_level = subscription_level
            db.session.commit()
            return user
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        # Handle the exception, possibly logging it
        return None
