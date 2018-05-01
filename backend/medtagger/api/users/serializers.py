"""Module containing serializers for users endpoints."""
from flask_restplus import fields

from medtagger.api import api

user = api.model('User model', {
    'id': fields.Integer(attribute='id', description='User\'s id'),
    'email': fields.String(attribute='email', description='Email address'),
    'firstName': fields.String(attribute='first_name', description='First name'),
    'lastName': fields.String(attribute='last_name', description='Last name'),
    'role': fields.String(attribute='role.name', description='User\'s role'),
    'skipTutorial': fields.Boolean(attribute='skip_tutorial', description='Should tutorial be skipped?'),
})
users_list = api.model('Users list', {
    'users': fields.List(fields.Nested(user)),
})
