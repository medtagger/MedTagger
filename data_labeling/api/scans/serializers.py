"""Module responsible for storage of serializers used in Scans endpoints"""
from flask_restplus import reqparse, fields

from data_labeling.api import api
from data_labeling.types import ScanID


random_scan = api.model('Random scan model', {
    'scan_id': fields.String(description='Scan\'s ID'),
    'slices_begin': fields.Integer(description='First slice index (including) used for labeling'),
    'slices_end': fields.Integer(description='Last slice index (excluding) used for labeling'),
    'total_number_of_slices': fields.Integer(description='Total number of slices in given scan'),
})

rectangle_label = api.model('Rectangle label for given scan', {
    'scan_id': fields.String(description='Scan\'s ID', required=True),
    'x': fields.Float(description='Label\'s X position', min=0.0, max=1.0, required=True),
    'y': fields.Float(description='Label\'s Y position', min=0.0, max=1.0, required=True),
    'z': fields.Float(description='Label\'s Z position', min=0.0, max=1.0, required=True),
    'width': fields.Float(description='Label\'s width', min=0.0, max=1.0, required=True),
    'height': fields.Float(description='Label\'s height', min=0.0, max=1.0, required=True),
    'depth': fields.Float(description='Label\'s depth', min=0.0, max=1.0, required=True),
})


slices_arguments = reqparse.RequestParser()
slices_arguments.add_argument('scan_id', type=ScanID, required=True, help='Scan\'s ID')
slices_arguments.add_argument('begin', type=int, required=True, help='First slice index (included)')
slices_arguments.add_argument('end', type=int, required=True, help='Last slice index (excluded)')
