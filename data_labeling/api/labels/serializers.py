"""Module responsible for storage of serializers used in Labels endpoints"""
from flask_restplus import fields

from data_labeling.api import api
from data_labeling.database.models import LabelStatus


in__label_status = api.model("Status for label", {
    'status': fields.String(description='New status for label', enum=[status.name for status in LabelStatus],
                            required=True),
})

out__label_selection = api.model('Label Selection', {
    'x': fields.Float(description='Selection\'s X position', min=0.0, max=1.0, attribute='position_x'),
    'y': fields.Float(description='Selection\'s Y position', min=0.0, max=1.0, attribute='position_y'),
    'slice_index': fields.Integer(description='Slice\'s order index', min=0),
    'width': fields.Float(description='Selection\'s width', min=0.0, max=1.0, attribute='shape_width'),
    'height': fields.Float(description='Selection\'s height', min=0.0, max=1.0, attribute='shape_height'),
})

out__label_status = api.model('Label status and ID', {
    'label_id': fields.String(description='Label\'s ID', attribute='id'),
    'status': fields.String(description='Status of the label', attribute='status.name'),
})

out__label = api.inherit('Label model', out__label_status, {
    'scan_id': fields.String(description='Scan\'s ID'),
    'selections': fields.List(fields.Nested(out__label_selection)),
})
