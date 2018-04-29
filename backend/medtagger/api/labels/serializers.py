"""Module responsible for storage of serializers used in Labels endpoints."""
from flask_restplus import fields

from medtagger.api import api
from medtagger.database.models import LabelVerificationStatus, LabelElementStatus

in__label_status = api.model("Status for label", {
    'status': fields.String(description='New status for label',
                            enum=[status.name for status in LabelVerificationStatus],
                            required=True),
})

out__label_element = api.model('Label Element', {
    'x': fields.Float(description='Element\'s X position', min=0.0, max=1.0, attribute='position_x'),
    'y': fields.Float(description='Element\'s Y position', min=0.0, max=1.0, attribute='position_y'),
    'slice_index': fields.Integer(description='Slice\'s order index', min=0),
    'width': fields.Float(description='Element\'s width', min=0.0, max=1.0, attribute='shape_width'),
    'height': fields.Float(description='Element\'s height', min=0.0, max=1.0, attribute='shape_height'),
    'binary_mask': fields.String(description='Element\'s binary mask'),
    'tag': fields.String(description='Element\'s tag', attribute='tag.key'),
    'status': fields.String(description='Element\'s status', attribute='status.value',
                            enum=[status.name for status in LabelElementStatus]),
})

out__label_status = api.model('Label status and ID', {
    'label_id': fields.String(description='Label\'s ID', attribute='id'),
    'status': fields.String(description='Status of the label', attribute='status.name'),
})

out__label = api.inherit('Label model', out__label_status, {
    'scan_id': fields.String(description='Scan\'s ID'),
    'elements': fields.List(fields.Nested(out__label_element)),
    'labeling_time': fields.Float(description='Time in seconds that user spent on labeling'),
})
