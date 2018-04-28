"""Module responsible for defining endpoints for users administration."""
from typing import Any

from flask import request
from flask_restplus import Resource

from medtagger.api import api
from medtagger.api.users import serializers
from medtagger.api.users.business import get_all_users, set_user_role, set_user_info
from medtagger.api.utils import get_current_user
from medtagger.api.security import login_required, role_required

users_ns = api.namespace('users', 'Users management')


@users_ns.route('/')
class GetUsers(Resource):
    """Get all users endpoint."""

    @staticmethod
    @login_required
    @role_required('admin')
    @users_ns.marshal_with(serializers.users_list)
    @users_ns.doc(security='token')
    def get() -> Any:
        """Get all users endpoint."""
        users = get_all_users()
        return {'users': users}, 200


@users_ns.route('/<int:user_id>/role')
class SetRole(Resource):
    """Set user's role."""

    @staticmethod
    @login_required
    @role_required('admin')
    @users_ns.doc(security='token')
    def put(user_id: int) -> Any:
        """Set user's role."""
        set_user_role(user_id, request.json['role'])
        return {}, 204


@users_ns.route('/info')
class GetUserInfo(Resource):
    """Get current user information."""

    @staticmethod
    @login_required
    @users_ns.marshal_with(serializers.user)
    @users_ns.doc(security='token')
    @users_ns.doc(responses={200: 'Successfully retrieved data.'})
    def get() -> Any:
        """Get user info."""
        user = get_current_user()
        return user, 200

@users_ns.route('/<int:user_id>/')
class SetUserInfo(Resource):
    """Set user's information (first name and last name)"""

    @staticmethod
    @login_required
    @users_ns.doc(security='token')
    def put(user_id: int) -> Any:
        """Set user info."""
        set_user_info(user_id, request.json['firstName'], request.json['lastName'])
        return {}, 204