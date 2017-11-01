"""Module containg serializers for user endpoints"""
from flask_restplus import fields

from data_labeling.api import api

new_user = api.model('New user model', {
    'email': fields.String(required=True, min_length=1),
    'password': fields.String(required=True, min_length=8),
    'firstName': fields.String(required=True, min_length=1),
    'lastName': fields.String(required=True, min_length=1)
})

sign_in = api.model('Sign in model', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

user_info = api.model('User info model', {
    'email': fields.String(attribute='email', description='Email address'),
    'firstName': fields.String(attribute='first_name', description='First name'),
    'lastName': fields.String(attribute='last_name', description='Last name')
})
