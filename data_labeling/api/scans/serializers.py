"""Module responsible for storage of serializers used in Scans endpoints"""
from flask_restplus import reqparse, fields

from data_labeling.api import api


new_scan = api.model('New scan', {
    'scan_id': fields.String(description='Scan\'s ID'),
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


slices_arguments = reqparse.RequestParser()
slices_arguments.add_argument('begin', type=int, required=True, help='First slice index (included)')
slices_arguments.add_argument('count', type=int, required=True, help='Number of slices that user wants to fetch')
