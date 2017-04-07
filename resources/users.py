
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

            # verifies user and password
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

api_auth.add_resource(RegisterAPI, '/auth/register', endpoint='register')
api_auth.add_resource(LoginAPI, '/auth/login', endpoint='login')

