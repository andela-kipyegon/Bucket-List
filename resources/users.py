
from flask import Flask, abort, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, inputs
from app import db
from models import Users

auth_blueprint = Blueprint('auth', __name__)

api_auth = Api(auth_blueprint)


class RegisterAPI(Resource):
    """Register Resource"""

    def __init__(self):
        """ constructer for Register API Reosurce """

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=inputs.regex(r'^[a-zA-Z]{3,}$'),
                                   required=True, help='Invalid first name', nullable=False,
                                   location='json')
        self.reqparse.add_argument('last_name', help='Invalid second name',
                                   required=True, type=inputs.regex(r'^[a-zA-Z]{3,}$'),
                                   location='json')
        self.reqparse.add_argument('email', type=inputs.regex(r"[^@]+@[^@]+\.[^@]+"), required=True,
                                   help="Invalid email", location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                   location='json')
        self.reqparse.add_argument('confirm_password', type=str, default="",
                                   location='json')

    def post(self):
        """ lets one register to the API """

        args = self.reqparse.parse_args()
        user = Users.query.filter_by(email=args['email']).first()
        if not user:
            try:
                user = Users(
                    first_name=args['first_name'],
                    last_name=args['last_name'],
                    email=args['email'],
                    password=args['password']
                )
                # insert the user
                user.hash_password(args['password'])
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.generate_auth_token()
                response = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }

                return response, 201
            except Exception as e:
                response = {
                    'status': 'fail' + str(e),
                    'message': 'Some error occurred. Please try again.'
                }
                return response, 500
        else:
            response = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response, 202



class LoginAPI(Resource):
    """Login Resource"""

    def __init__(self):
        """
        constructor for  LoginAPI
        """

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('password', type=str, default="",
                                   location='json')

    def post(self):
        """"
         fxn to allow Login into the API
        """

        args = self.reqparse.parse_args()
        try:
            user = Users.query.filter_by(email=args['email']).first()

            if user and user.verify_password(args['password']):
                auth_token = user.generate_auth_token()
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'auth_token': auth_token.decode()
                }
                return response, 200
            else:
                response = {
                    'status': 'fail',
                    'message': 'Invalid user or Password mismatch.'
                }
                return response, 404
        except:

            response = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response, 500

class UserAPI(Resource):
    "gets the user status"

    def get(self):
        """
        gets the status of the currently logged in user
        """
        import pdb; pdb.set_trace()
        auth_header = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            user = Users.verify_auth_token(auth_token)

            if user:
                response = {
                    'status': 'success',
                    'data': {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                }
                return response, 200
            response = {
                'status': 'fail',
                'message': 'logged out'
            }
            return response, 401
        response = {
            'status': 'fail',
            'message': 'please provide the token'
            }
        return response, 401

api_auth.add_resource(UserAPI, '/auth/status', endpoint='user')
api_auth.add_resource(RegisterAPI, '/auth/register', endpoint='register')
api_auth.add_resource(LoginAPI, '/auth/login', endpoint='login')
