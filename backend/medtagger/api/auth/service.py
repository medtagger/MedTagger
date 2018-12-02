"""Module responsible for definition of Auth service."""
from typing import Any

from flask import request
from flask_restplus import Resource

from medtagger.api import api
from medtagger.api.auth.business import create_user, sign_in_user
from medtagger.api.auth import serializers

auth_ns = api.namespace('auth', 'Auth methods')


@auth_ns.route('/register')
class Register(Resource):
    """Register user endpoint."""

    @staticmethod
    @api.expect(serializers.new_user)
    @api.doc(responses={201: 'User created', 400: 'Invalid arguments'})
    def post() -> Any:
        """Register the user."""
        user = request.json
        token = create_user(user['email'], user['password'], user['firstName'], user['lastName'])
        return {'token': token}, 201


@auth_ns.route('/sign-in')
class SignIn(Resource):
    """Sign in endpoint."""

    @staticmethod
    @api.expect(serializers.sign_in)
    @api.doc(responses={200: 'Signed in', 400: 'User does not exist or wrong password was provided'})
    def post() -> Any:
        """Sign in the user."""
        sign_in = request.json
        token = sign_in_user(sign_in['email'], sign_in['password'])
        return {"token": token}, 200
