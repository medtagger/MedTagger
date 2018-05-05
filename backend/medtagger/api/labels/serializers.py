"""Module responsible for storage of serializers used in Labels endpoints."""
from flask_restplus import fields

from medtagger.api import api
from medtagger.database.models import LabelVerificationStatus, LabelElementStatus, LabelTool

in__label_status = api.model("Status for label", {
    'status': fields.String(description='New status for label',
                            enum=[status.name for status in LabelVerificationStatus],
                            required=True),
})

elements_schema = {
    'type': 'object',
    'properties': {
        'elements': {
            'oneOf': [
                {'$ref': '#/definitions/rectangular_label_element_schema'},
            ]
        }
    },
    'definitions': {
        'rectangular_label_element_schema': {
            'properties': {
                'x': {'type': 'number'},
                'y': {'type': 'number'},
                'width': {'type': 'number'},
                'height': {'type': 'number'},
                'slice_index': {'type': 'integer'},
                'tag': {'type': 'string'},
                'tool': {'enum': [tool.name for tool in LabelTool]},
                'status': {'enum': [status.name for status in LabelElementStatus]},
            },
            'required': ['x', 'y', 'width', 'height', 'slice_index', 'tag', 'tool', 'status'],
        }
    }
}

out__label_status = api.model('Label status and ID', {
    'label_id': fields.String(description='Label\'s ID', attribute='id'),
    'status': fields.String(description='Status of the label', attribute='status.name'),
})

out__label = api.inherit('Label model', out__label_status, {
    'scan_id': fields.String(description='Scan\'s ID'),
    'elements': fields.List(fields.Raw),
    'labeling_time': fields.Float(description='Time in seconds that user spent on labeling'),
    'status': fields.String(description='Label\'s status', enum=[status.name for status in LabelVerificationStatus]),
})
