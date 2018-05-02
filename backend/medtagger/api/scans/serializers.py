"""Module responsible for storage of serializers used in Scans endpoints."""
from flask_restplus import reqparse, fields

from medtagger.api import api
from medtagger.database.models import LabelVerificationStatus

in__new_scan = api.model('New Scan model', {
    'category': fields.String(description='Scan\'s category', required=True),
    'number_of_slices': fields.Integer(description='Number of Slices that will be uploaded', required=True),
})

in__label_element = api.model('Label\'s Element model', {
    'x': fields.Float(description='Element\'s X position', min=0.0, max=1.0, required=True),
    'y': fields.Float(description='Element\'s Y position', min=0.0, max=1.0, required=True),
    'slice_index': fields.Integer(description='Slice\'s order index', min=0, required=True),
    'width': fields.Float(description='Element\'s width', min=0.0, max=1.0, required=True),
    'height': fields.Float(description='Element\'s height', min=0.0, max=1.0, required=True),
    'binary_mask': fields.String(description='Selection\'s binary mask'),
    'tag': fields.String(description='Element\'s tag'),
    'status': fields.String(description='Element\'s status', enum=[status.name for status in LabelVerificationStatus]),
})

in__label_tag_element = api.model('Label Element model', {
    'key': fields.String(),
    'name': fields.String(),
})

in__label = api.model('Label model', {
    'elements': fields.List(fields.Nested(in__label_element)),
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
    'scan_id': fields.String(description='Scan\'s ID'),
    'number_of_slices': fields.Integer(description='Total number of slices in given scan'),
})

out__label = api.model('Newly created Label model', {
    'label_id': fields.String(description='Label\'s ID', attribute='id'),
    'owner_id': fields.Integer(description='ID of user that created label'),
    'labeling_time': fields.Float(description='Time in seconds that user spent on labeling'),
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
