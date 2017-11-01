"""Module responsible for definition of Labels service available via HTTP REST API"""
from typing import Any
from flask import request
from flask_restplus import Resource

from data_labeling.api.labels.business import get_random_label
from data_labeling.types import LabelID
from data_labeling.api import api
from data_labeling.api.labels import serializers
from data_labeling.api.labels.business import change_label_status

labels_ns = api.namespace('labels', 'Methods related with labels')


@labels_ns.route('/random')
class Random(Resource):
    """Endpoint that returns random label with status NOT_VERIFIED"""

    @staticmethod
    @labels_ns.marshal_with(serializers.label)
    @labels_ns.doc(description='Returns random label with NOT_VERIFIED status.')
    @labels_ns.doc(responses={200: 'Success', 404: 'Could not find label'})
    def get() -> Any:
        """Method responsible for returning random label's metadata"""
        label = get_random_label()
        if not label:
            return "Label not found", 404
        return label


@labels_ns.route('/<string:label_id>/status')
@labels_ns.param('label_id', 'Label identifier')
class ChangeLabelStatus(Resource):
    """Endpoint that enables change of the label status"""

    @staticmethod
    @labels_ns.expect(serializers.status)
    @labels_ns.marshal_with(serializers.label_status)
    @labels_ns.doc(description='Changes the status of the given label.')
    @labels_ns.doc(
        responses={200: 'Successfully changed status', 400: 'Invalid arguments', 404: 'Could not find label'})
    def put(label_id: LabelID) -> Any:
        """Method responsible for changing the state of the label"""
        payload = request.json
        status = payload.get('status')
        label = change_label_status(label_id, status)
        return label
