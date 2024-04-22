from flask_restx import Namespace, Resource, fields, reqparse
from services.loginService import loginService
from app import api2

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email address', location='json')
login_parser.add_argument('password', type=str, required=True, help='Password', location='json')

@api2.route('/login')
class LoginResource(Resource):
    @api2.expect(login_parser)
    def post(self):
        """Login a user and return a token along with user ID and email"""
        args = login_parser.parse_args()
        login_response = loginService(email=args['email'], password=args['password'])
        
        if login_response is None:
            # This means there was an error processing the request or invalid credentials
            api2.abort(500, 'Internal server error')
        elif login_response:
            # Response will now include the token, user_id, and email
            return {
                'message': 'Login successful',
                'token': login_response['token'],
                'user_id': login_response['user_id'],
                'email': login_response['email']
            }, 200
        else:
            return {'message': 'Invalid credentials'}, 401
