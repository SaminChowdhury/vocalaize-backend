# signupController.py

from flask_restx import Resource, fields, reqparse
from werkzeug.security import generate_password_hash
from app import api2
from services.signupService import signupService

user_model = api2.model(
    'User',
    {
        'id': fields.Integer(description='The user unique identifier'),
        'email': fields.String(required=True, description='The user email'),
        'password': fields.String(required=True, description='The user password', attribute=lambda x: None),  # Avoid returning password
    }
)

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('email', type=str, required=True, help='Email address', location='json')
signup_parser.add_argument('password', type=str, required=True, help='Password', location='json')

@api2.route('/signup')
class SignupResource(Resource):
    @api2.expect(signup_parser)
    @api2.marshal_with(user_model, envelope='data', code=201)
    def post(self):
        """Sign up a new user"""
        args = signup_parser.parse_args()
        hashed_password = generate_password_hash(args['password'], method='scrypt')
        user = signupService(email=args['email'], password=hashed_password)
        if user:
            return user, 201
        else:
            api2.abort(400, 'Failed to create user')
