"""Module responsible for defining endpoints for user management"""
from typing import Any

from flask import request
from flask_restplus import Resource

from data_labeling.api import api
from data_labeling.api.user import serializers
from data_labeling.api.user.business import create_user

user_ns = api.namespace('users', 'User management methods')


@user_ns.route('/register')
class Register(Resource):
    """Register user endpoint"""
    @staticmethod
    @api.expect(serializers.new_user)
    @api.doc(responses={201: 'User created', 400: 'Invalid arguments'})
    def post() -> Any:
        """Register user endpoint post method"""
        new_user = request.json
        user_id = create_user(new_user['username'], new_user['password'])
        return {'id': user_id}, 201
