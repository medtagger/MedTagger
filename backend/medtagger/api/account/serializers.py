"""Module containing serializers for user's account endpoints."""
from flask_restplus import fields

from medtagger.api import api

new_user = api.model('New user model', {
    'email': fields.String(required=True, min_length=1),
    'password': fields.String(required=True, min_length=8),
    'firstName': fields.String(required=True, min_length=1),
    'lastName': fields.String(required=True, min_length=1),
})

sign_in = api.model('Sign in model', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

user_info = api.model('User info model', {
    'id': fields.Integer(attribute='id', description='User\'s id'),
    'email': fields.String(attribute='email', description='Email address'),
    'firstName': fields.String(attribute='first_name', description='First name'),
    'lastName': fields.String(attribute='last_name', description='Last name'),
    'role': fields.String(attribute='role', description='User\'s role'),
})
