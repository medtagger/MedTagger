"""Module containg serializers for user endpoints"""
from flask_restplus import fields

from data_labeling.api import api

new_user = api.model('New user model', {
    'username': fields.String(required=True),
    'password': fields.String(required=True, min_length=8)
})
