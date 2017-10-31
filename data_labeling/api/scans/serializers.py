"""Module responsible for storage of serializers used in Scans endpoints"""
from flask_restplus import reqparse, fields

from data_labeling.api import api


new_scan_request = api.model('New scan request', {
    'category': fields.String(description='Scan\'s category')
})

new_scan_response = api.model('New scan response', {
    'scan_id': fields.String(description='Scan\'s ID'),
})

scan_category = api.model('New scan category model', {
    'key': fields.String(),
    'name': fields.String(),
    'image_path': fields.String(),
})

random_scan = api.model('Random scan model', {
    'scan_id': fields.String(description='Scan\'s ID'),
    'number_of_slices': fields.Integer(description='Total number of slices in given scan'),
})

label_selection = api.model('User\'s Label Selection', {
    'x': fields.Float(description='Selection\'s X position', min=0.0, max=1.0, required=True),
    'y': fields.Float(description='Selection\'s Y position', min=0.0, max=1.0, required=True),
    'slice_index': fields.Integer(description='Slice\'s order index', min=0, required=True),
    'width': fields.Float(description='Selection\'s width', min=0.0, max=1.0, required=True),
    'height': fields.Float(description='Selection\'s height', min=0.0, max=1.0, required=True),
})

label = api.model('Label for given scan', {
    'selections': fields.List(fields.Nested(label_selection)),
})

accepted = api.model('Accepted for asynchronous processing', {
    'accepted': fields.Boolean(description='Should be True if everything is all right'),
})


random_scan_arguments = reqparse.RequestParser()
random_scan_arguments.add_argument('category', type=str, required=True, help='Scan\'s category')
