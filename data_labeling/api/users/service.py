"""Module responsible for defining endpoints for users administration"""
from typing import Any

from flask import request
from flask_login import login_required
from flask_restplus import Resource

from data_labeling.api import api
from data_labeling.api.users import serializers
from data_labeling.api.users.business import get_all_users, set_user_role

users_ns = api.namespace('users', 'Users management')


@users_ns.route('')
class Register(Resource):
    """Get all users endpoint"""

    @staticmethod
    @api.marshal_with(serializers.user_info_list)
    def get() -> Any:
        """Get all users endpoint"""
        users = get_all_users()
        user_infos = list(map(lambda user: user._asdict(), users))
        return {'users': user_infos}, 200


@users_ns.route('/<int:user_id>/role')
class SetRole(Resource):
    """Set user's role"""

    @staticmethod
    @login_required
    def put(user_id: int) -> Any:
        """Set user's role"""
        set_user_role(user_id, request.json['role'])
        return {}, 204
