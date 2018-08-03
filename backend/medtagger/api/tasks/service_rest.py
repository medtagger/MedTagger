"""Module responsible for definition of Tasks service available via HTTP REST API."""
from typing import Any

from flask import request
from flask_restplus import Resource

from medtagger.api import api
from medtagger.api.tasks import business, serializers
from medtagger.api.security import login_required, role_required

tasks_ns = api.namespace('tasks', 'Methods related with tasks')


@tasks_ns.route('')
class Tasks(Resource):
    """Endpoint that manages tasks."""

    @staticmethod
    @login_required
    @tasks_ns.marshal_with(serializers.out__task)
    @tasks_ns.doc(security='token')
    @tasks_ns.doc(description='Return all available tasks.')
    @tasks_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Return all available tasks."""
        return business.get_tasks()

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @tasks_ns.expect(serializers.in__task)
    @tasks_ns.marshal_with(serializers.out__task)
    @tasks_ns.doc(security='token')
    @tasks_ns.doc(description='Create new Task.')
    @tasks_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Create new Task."""
        payload = request.json

        key = payload['key']
        name = payload['name']
        image_path = payload['image_path']
        categories_ids = payload['categories_ids']

        return business.create_task(key, name, image_path, categories_ids), 201
