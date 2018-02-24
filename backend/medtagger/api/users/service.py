"""Module responsible for defining endpoints for users administration."""
from typing import Any

from flask import request
from flask_login import login_required
from flask_restplus import Resource

from medtagger.api import api
from medtagger.api.users import serializers
from medtagger.api.users.business import get_all_users, set_user_role, get_current_user_info

users_ns = api.namespace('users', 'Users management')


@users_ns.route('/')
class GetUsers(Resource):
    """Get all users endpoint."""

    @staticmethod
    @api.marshal_with(serializers.user_info_list)
    def get() -> Any:
        """Get all users endpoint."""
        users = get_all_users()
        return {'users': users}, 200


@users_ns.route('/<int:user_id>/role')
class SetRole(Resource):
    """Set user's role."""

    @staticmethod
    @login_required
    def put(user_id: int) -> Any:
        """Set user's role."""
        set_user_role(user_id, request.json['role'])
        return {}, 204


@users_ns.route('/info')
class GetUserInfo(Resource):
    """Get user info endpoint."""

    @staticmethod
    @login_required
    @api.marshal_with(serializers.user_info)
    @api.doc(responses={200: 'Successfully retrieved data.'})
    def get() -> Any:
        """Get user info."""
        user_info = get_current_user_info()
        return user_info, 200
