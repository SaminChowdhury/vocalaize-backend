# controllers/subscriptionController.py
from flask_restx import Namespace, Resource
from services.getSubscriptionLevelService import get_subscription_service
from app import api2


@api2.route('/<int:user_id>/subscription')
class UserSubscriptionResource(Resource):
    def get(self, user_id):
        """Retrieve subscription level for a specific user"""
        result = get_subscription_service(user_id)
        if 'error' in result:
            return result, 404 if result.get('error') == 'User not found' else 500
        return result, 200
