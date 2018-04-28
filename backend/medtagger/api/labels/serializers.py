"""Module responsible for storage of serializers used in Labels endpoints."""
from flask_restplus import fields

from medtagger.api import api
from medtagger.database.models import LabelStatus


in__label_status = api.model("Status for Label", {
    'status': fields.String(description='New status for Label', enum=[status.name for status in LabelStatus],
                            required=True),
})

in__action_response = api.model("Response for Action", {})

out__label_selection = api.model('Label Selection', {
    'x': fields.Float(description='Selection\'s X position', min=0.0, max=1.0, attribute='position_x'),
    'y': fields.Float(description='Selection\'s Y position', min=0.0, max=1.0, attribute='position_y'),
    'slice_index': fields.Integer(description='Slice\'s order index', min=0),
    'width': fields.Float(description='Selection\'s width', min=0.0, max=1.0, attribute='shape_width'),
    'height': fields.Float(description='Selection\'s height', min=0.0, max=1.0, attribute='shape_height'),
    'binary_mask': fields.String(description='Selection\'s binary mask'),
})

out__label_status = api.model('Label status and ID', {
    'label_id': fields.String(description='Label\'s ID', attribute='id'),
    'status': fields.String(description='Status of the label', attribute='status.name'),
})

out__label = api.inherit('Label model', out__label_status, {
    'scan_id': fields.String(description='Scan\'s ID'),
    'selections': fields.List(fields.Nested(out__label_selection)),
    'labeling_time': fields.Float(description='Time in seconds that user spent on labeling'),
})

out__action = api.model('Action model', {
    'action_id': fields.Integer(description='Action\'s ID', attribute='id'),
    'action_type': fields.String(description='Action\'s Type'),
    'details': fields.Raw(attribute=lambda action: action.get_details()),
})

out__action_response = api.model('Action Response model', {
    'response_id': fields.Integer(description='Action Response\'s ID', attribute='id'),
    'action_id': fields.Integer(description='Action\'s ID', attribute='action.id'),
    'action_type': fields.String(description='Action\'s Type', attribute='action.action_type'),
    'details': fields.Raw(attribute=lambda action_response: action_response.get_details()),
})
