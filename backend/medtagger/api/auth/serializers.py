"""Module responsible for storage of serializers used in Auth endpoints."""
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
