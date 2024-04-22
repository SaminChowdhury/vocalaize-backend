# controllers/tokenValidationController.py
from flask_restx import Namespace, Resource, fields, reqparse
from services.authValidService import validate_token_service
from app import api2


token_validation_parser = reqparse.RequestParser()
token_validation_parser.add_argument('token', type=str, required=True, help='JWT token', location='headers')

@api2.route('/validate-token')
class TokenValidationResource(Resource):
    @api2.expect(token_validation_parser)
    def get(self):
        """Validate a JWT token and return user info if valid"""
        args = token_validation_parser.parse_args()
        token = args['token']
        result = validate_token_service(token)
        if result['valid']:
            return {'message': 'Token is valid', 'user_info': result['user_info']}, 200
        else:
            return {'message': 'Token is invalid', 'error': result['error']}, 401
