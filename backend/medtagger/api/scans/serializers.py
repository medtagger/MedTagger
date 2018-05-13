"""Module responsible for storage of serializers used in Scans endpoints."""
from flask_restplus import reqparse, fields

from medtagger.api import api
from medtagger.definitions import ScanStatus, LabelVerificationStatus, LabelTool

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
        ],
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
            },
            'required': ['x', 'y', 'width', 'height', 'slice_index', 'tag', 'tool'],
        },
    },
}

in__label_tag_element = api.model('Label Element model', {
    'key': fields.String(),
    'name': fields.String(),
})

in__label = api.model('Label model', {
    'elements': fields.List(fields.Raw),
    'labeling_time': fields.Float(description='Time in seconds that user spent on labeling'),
})

in__scan_category = api.model('New Scan Category model', {
    'key': fields.String(),
    'name': fields.String(),
    'image_path': fields.String(),
})

out__scan_category = api.model('Scan Category model', {
    'key': fields.String(),
    'name': fields.String(),
    'image_path': fields.String(),
    'tags': fields.List(fields.Nested(in__label_tag_element), attribute='available_tags'),
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
args__random_scan.add_argument('category', type=str, required=True, help='Scan\'s category')
