"""Module responsible for storage of serializers used in Scans endpoints"""
from flask_restplus import reqparse, fields

from data_labeling.api import api


new_scan = api.model('New scan', {
    'scan_id': fields.String(description='Scan\'s ID'),
})

random_scan = api.model('Random scan model', {
    'scan_id': fields.String(description='Scan\'s ID'),
    'slices_begin': fields.Integer(description='First slice index (including) used for labeling'),
    'slices_count': fields.Integer(description='Number of slices that user should label'),
    'total_number_of_slices': fields.Integer(description='Total number of slices in given scan'),
})

cuboid_label = api.model('Cuboid label for given scan', {
    'x': fields.Float(description='Label\'s X position', min=0.0, max=1.0, required=True),
    'y': fields.Float(description='Label\'s Y position', min=0.0, max=1.0, required=True),
    'z': fields.Float(description='Label\'s Z position', min=0.0, max=1.0, required=True),
    'width': fields.Float(description='Label\'s width', min=0.0, max=1.0, required=True),
    'height': fields.Float(description='Label\'s height', min=0.0, max=1.0, required=True),
    'depth': fields.Float(description='Label\'s depth', min=0.0, max=1.0, required=True),
})

accepted = api.model('Accepted for asynchronous processing', {
    'accepted': fields.Boolean(description='Should be True if everything is all right'),
})


slices_arguments = reqparse.RequestParser()
slices_arguments.add_argument('begin', type=int, required=True, help='First slice index (included)')
slices_arguments.add_argument('count', type=int, required=True, help='Number of slices that user wants to fetch')
