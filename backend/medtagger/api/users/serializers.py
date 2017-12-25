"""Module containg serializers for users endpoints."""
from flask_restplus import fields

from medtagger.api import api
from medtagger.api.account.serializers import user_info

user_info_list = api.model('User info list', {
    'users': fields.List(fields.Nested(user_info)),
})
