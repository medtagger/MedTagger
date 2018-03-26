"""Module responsible for definition of Labels service available via HTTP REST API."""
from typing import Any

from flask import request
from flask_restplus import Resource

from medtagger.types import LabelID
from medtagger.database.models import LabelStatus
from medtagger.api import api, InvalidArgumentsException, NotFoundException
from medtagger.api.labels import business, serializers
from medtagger.api.security import login_required, role_required


labels_ns = api.namespace('labels', 'Methods related with labels')


@labels_ns.route('/random')
class Random(Resource):
    """Endpoint that returns random label with status NOT_VERIFIED."""

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @labels_ns.marshal_with(serializers.out__label)
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
    @labels_ns.doc(description='Changes the status of the given label.')
    @labels_ns.doc(responses={200: 'Successfully changed status', 400: 'Invalid arguments',
                              404: 'Could not find given Label'})
    def put(label_id: LabelID) -> Any:
        """Change the state of the label."""
        payload = request.json
        raw_status = payload['status']
        try:
            status = LabelStatus[raw_status]
        except KeyError:
            raise InvalidArgumentsException('Label Status "{}" is not available.'.format(raw_status))

        return business.change_label_status(label_id, status)
