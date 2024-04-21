# controllers/loginController.py
from app import api2
from flask_restx import Namespace, Resource, fields, reqparse
from services.loginService import loginService


login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email address', location='json')
login_parser.add_argument('password', type=str, required=True, help='Password', location='json')

@api2.route('/login')
class LoginResource(Resource):
    @api2.expect(login_parser)
    def post(self):
        """Login a user and return a token"""
        args = login_parser.parse_args()
        success = loginService(email=args['email'], password=args['password'])
        
        if success is None:
            # This means there was an error processing the request
            api2.abort(500, 'Internal server error')
        elif success:
            # Assume a token is generated and returned upon successful login
            return {'message': 'Login successful'}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
