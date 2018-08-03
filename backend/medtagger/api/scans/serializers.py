"""Module responsible for storage of serializers used in Scans endpoints."""
from flask_restplus import reqparse, fields

from medtagger.api import api
from medtagger.api.tasks.serializers import out__task
from medtagger.definitions import ScanStatus, LabelVerificationStatus

in__new_scan = api.model('New Scan model', {
    'category': fields.String(description='Scan\'s category', required=True),
    'number_of_slices': fields.Integer(description='Number of Slices that will be uploaded', required=True),
})

elements_schema = {
    'type': 'array',
    "items": {
        "type": "object",
        'oneOf': [
            {'$ref': '#/definitions/rectangular_label_element_schema'},
            {'$ref': '#/definitions/brush_label_element_schema'},
            {'$ref': '#/definitions/point_label_element_schema'},
            {'$ref': '#/definitions/chain_label_element_schema'},
        ],
    },
    'definitions': {
        'rectangular_label_element_schema': {
            'properties': {
                'x': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                'y': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                'width': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                'height': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                'slice_index': {'type': 'integer'},
                'tag': {'type': 'string'},
                'tool': {'type': 'string', 'pattern': 'RECTANGLE'},
            },
            'required': ['x', 'y', 'width', 'height', 'slice_index', 'tag', 'tool'],
            'additionalProperties': False,
        },
        'brush_label_element_schema': {
            'properties': {
                'width': {'type': 'integer', 'minimum': 0},
                'height': {'type': 'integer', 'minimum': 0},
                'image_key': {'type': 'string'},
                'slice_index': {'type': 'integer'},
                'tag': {'type': 'string'},
                'tool': {'type': 'string', 'pattern': 'BRUSH'},
            },
            'required': ['width', 'height', 'image_key', 'slice_index', 'tag', 'tool'],
            'additionalProperties': False,
        },
        'point_label_element_schema': {
            'properties': {
                'x': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                'y': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                'slice_index': {'type': 'integer'},
                'tag': {'type': 'string'},
                'tool': {'type': 'string', 'pattern': 'POINT'},
            },
            'required': ['x', 'y', 'slice_index', 'tag', 'tool'],
            'additionalProperties': False,
        },
        'chain_label_element_schema': {
            'properties': {
                'slice_index': {'type': 'integer'},
                'tag': {'type': 'string'},
                'tool': {'type': 'string', 'pattern': 'CHAIN'},
                'points': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'x': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                            'y': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                        },
                        'required': ['x', 'y'],
                        'additionalProperties': False,
                    },
                    'minItems': 2,
                },
                'loop': {'type': 'boolean'},
            },
            'required': ['points', 'slice_index', 'tag', 'tool', 'loop'],
            'additionalProperties': False,
        },
    },
}

in__label_model = api.model('Label model', {
    'elements': fields.List(fields.Raw, required=True),
    'labeling_time': fields.Float(description='Time in seconds that user spent on labeling', required=True),
    'task_id': fields.Integer(description='ID of the Task that label refers to', required=True),
})

in__label = api.parser()
in__label.add_argument('label', type=in__label_model, help='Label model object', location='form', required=True)

in__scan_category = api.model('New Scan Category model', {
    'key': fields.String(),
    'name': fields.String(),
    'image_path': fields.String(),
})

out__scan_category = api.model('Scan Category model', {
    'key': fields.String(),
    'name': fields.String(),
    'image_path': fields.String(),
    'tasks': fields.List(fields.Nested(out__task)),
})

out__scan = api.model('Scan model', {
    'scan_id': fields.String(description='Scan\'s ID', attribute='id'),
    'width': fields.Integer(description='Scan\'s width in Z axis'),
    'height': fields.Integer(description='Scan\'s height in Z axis'),
    'status': fields.String(description='Scan\'s status', enum=[status.name for status in ScanStatus],
                            attribute='status.name'),
    'number_of_slices': fields.Integer(description='Total number of Slices in given scan',
                                       attribute='declared_number_of_slices'),
})

out__label = api.model('Newly created Label model', {
    'label_id': fields.String(description='Label\'s ID', attribute='id'),
    'owner_id': fields.Integer(description='ID of user that created label'),
    'labeling_time': fields.Float(description='Time in seconds that user spent on labeling'),
    'status': fields.String(description='Label\'s status', enum=[status.name for status in LabelVerificationStatus]),
})

out__new_scan = api.model('Newly created Scan model', {
    'scan_id': fields.String(description='Scan\'s ID', attribute='id'),
    'owner_id': fields.Integer(description='ID of user that uploaded scan'),
})

out__new_slice = api.model('Newly created Slice model', {
    'slice_id': fields.String(description='Slice\'s ID', attribute='id'),
})

args__random_scan = reqparse.RequestParser()
args__random_scan.add_argument('task', type=str, required=True, help='Task\'s key')
