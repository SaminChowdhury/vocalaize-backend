# controllers/subscriptionController.py
from app import api2
from flask_restx import Namespace, Resource, reqparse
from services.subscriptionLevelService import selectSubscriptionService


subscription_parser = reqparse.RequestParser()
subscription_parser.add_argument('subscription_level', type=str, required=True, help='Subscription level', location='json')

@api2.route('/user/<int:user_id>/subscription')
class SubscriptionResource(Resource):
    @api2.expect(subscription_parser)
    def post(self, user_id):
        """Select subscription level for a user after signup"""
        args = subscription_parser.parse_args()
        user = selectSubscriptionService(user_id=user_id, subscription_level=args['subscription_level'])
        if user:
            return {'message': 'Subscription level updated successfully.'}, 200
        else:
            return {'message': 'User not found or update failed.'}, 400
