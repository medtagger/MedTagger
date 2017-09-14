from flask import request
from flask_restplus import Resource

from data_labeling.api import api
from data_labeling.api.user import serializers
from data_labeling.api.user.business import create_user

user_ns = api.namespace('users', 'User management methods')


@user_ns.route('/register')
class Register(Resource):
    @api.expect(serializers.new_user, validate=True)
    @user_ns.doc(responses={201: 'User created', 400: 'Invalid arguments'})
    def post(self):
        new_user = request.json
        create_user(new_user['username'], new_user['password'])
        return {'id': id}, 201

