"""Module responsible for storage of serializers used in Scans endpoints"""
from flask_restplus import reqparse, fields

from data_labeling.api import api
from data_labeling.types import ScanID


metadata = api.model('Scan metadata model', {
    'number_of_slices': fields.Integer(description='Number of slices in given scan'),
})


metadata_arguments = reqparse.RequestParser()
metadata_arguments.add_argument('scan_id', type=ScanID, required=True, help='Scan\'s ID')

slices_arguments = reqparse.RequestParser()
slices_arguments.add_argument('scan_id', type=ScanID, required=True, help='Scan\'s ID')
slices_arguments.add_argument('begin', type=int, required=True, help='First slice index (included)')
slices_arguments.add_argument('end', type=int, required=True, help='Last slice index (excluded)')
