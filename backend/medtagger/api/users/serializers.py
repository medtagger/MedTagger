"""Module containing serializers for users endpoints."""
from flask_restplus import fields

from medtagger.api import api

user_info = api.model('User info model', {
    'id': fields.Integer(attribute='id', description='User\'s id'),
    'email': fields.String(attribute='email', description='Email address'),
    'firstName': fields.String(attribute='first_name', description='First name'),
    'lastName': fields.String(attribute='last_name', description='Last name'),
    'role': fields.String(attribute='role', description='User\'s role'),
})
user_info_list = api.model('User info list', {
    'users': fields.List(fields.Nested(user_info)),
})
