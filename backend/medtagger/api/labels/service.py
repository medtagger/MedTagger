"""Module responsible for definition of Labels service available via HTTP REST API."""
from typing import Any

from flask import request
from flask_restplus import Resource

from medtagger.types import LabelID, ActionID
from medtagger.definitions import LabelVerificationStatus
from medtagger.api import api, InvalidArgumentsException, NotFoundException
from medtagger.api.labels import business, serializers
from medtagger.api.security import login_required, role_required


labels_ns = api.namespace('labels', 'Methods related with labels')


@labels_ns.route('/<string:label_id>')
@labels_ns.param('label_id', 'Label identifier')
class Label(Resource):
    """Endpoint that returns Label for the given Label ID."""

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @labels_ns.marshal_with(serializers.out__label)
    @labels_ns.doc(security='token')
    @labels_ns.doc(description='Returns Label with given Label ID.')
    @labels_ns.doc(responses={200: 'Success', 404: 'Could not find Label'})
    def get(label_id: LabelID) -> Any:
        """Return Label for the given Label ID."""
        return business.get_label(label_id)


@labels_ns.route('/random')
class RandomLabel(Resource):
    """Endpoint that returns random label with status NOT_VERIFIED."""

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @labels_ns.marshal_with(serializers.out__label)
    @labels_ns.doc(security='token')
    @labels_ns.doc(description='Returns random label with NOT_VERIFIED status.')
    @labels_ns.doc(responses={200: 'Success', 404: 'Could not find any Label'})
    def get() -> Any:
        """Return random label's metadata."""
        label = business.get_random_label()
        if not label:
            raise NotFoundException('No Labels found.')
        return label


@labels_ns.route('/<string:label_id>/status')
@labels_ns.param('label_id', 'Label identifier')
class ChangeLabelStatus(Resource):
    """Endpoint that enables change of the label status."""

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @labels_ns.expect(serializers.in__label_status)
    @labels_ns.marshal_with(serializers.out__label_status)
    @labels_ns.doc(security='token')
    @labels_ns.doc(description='Changes the status of the given label.')
    @labels_ns.doc(responses={200: 'Successfully changed status', 400: 'Invalid arguments',
                              404: 'Could not find given Label'})
    def put(label_id: LabelID) -> Any:
        """Change the state of the label."""
        payload = request.json
        raw_status = payload['status']
        try:
            status = LabelVerificationStatus[raw_status]
        except KeyError:
            raise InvalidArgumentsException('Label Status "{}" is not available.'.format(raw_status))

        return business.change_label_status(label_id, status)


@labels_ns.route('/actions/<int:action_id>')
class ActionDetails(Resource):
    """Endpoint that handles all operations on Actions."""

    @staticmethod
    @login_required
    @labels_ns.marshal_with(serializers.out__action)
    @labels_ns.doc(security='token')
    @labels_ns.doc(description='Returns details about Action that user should do with Label.')
    @labels_ns.doc(responses={200: 'Success', 404: 'Could not find such Action'})
    def get(action_id: ActionID) -> Any:
        """Return details about given Action."""
        return business.get_action_details(action_id)

    @staticmethod
    @login_required
    @labels_ns.expect(serializers.in__action_response)
    @labels_ns.marshal_with(serializers.out__action_response)
    @labels_ns.doc(security='token')
    @labels_ns.doc(description='Add new Response for given Action.')
    @labels_ns.doc(responses={200: 'Success', 400: 'Invalid Action Response', 404: 'Could not find such Action'})
    def post(action_id: ActionID) -> Any:
        """Add new Response for given Action."""
        payload = request.json
        return business.add_action_response(action_id, payload)
