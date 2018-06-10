"""Module responsible for storage of serializers used in Labels endpoints."""
from flask_restplus import fields

from medtagger.api import api
from medtagger.database.models import RectangularLabelElement, BrushLabelElement, PointLabelElement
from medtagger.definitions import LabelVerificationStatus, LabelElementStatus, LabelTool

in__label_status = api.model("Status for label", {
    'status': fields.String(description='New status for label',
                            enum=[status.name for status in LabelVerificationStatus],
                            required=True),
})

out__common_label_element = api.model('Common Label Element model', {
    'label_element_id': fields.String(description='Label Element\'s ID', attribute='id'),
    'slice_index': fields.Integer(description='Slice\'s order index', min=0),
    'tag': fields.String(description='Element\'s tag', attribute='tag.key'),
    'tool': fields.String(description='Element\'s tool', attribute='tool.value',
                          enum=[tool.name for tool in LabelTool]),
    'status': fields.String(description='Element\'s status', attribute='status.value',
                            enum=[status.name for status in LabelElementStatus]),
})

out__rectangular_label_element = api.inherit('Rectangular Label Element model', out__common_label_element, {
    'x': fields.Float(description='Element\'s X position', min=0.0, max=1.0),
    'y': fields.Float(description='Element\'s Y position', min=0.0, max=1.0),
    'width': fields.Float(description='Element\'s width', min=0.0, max=1.0),
    'height': fields.Float(description='Element\'s height', min=0.0, max=1.0),
})

out__brush_label_element = api.inherit('Brush Label Element model', out__common_label_element, {
    'width': fields.Integer(description='Image\'s width', min=0),
    'height': fields.Integer(description='Image\'s height', min=0),
})

out__point_label_element = api.inherit('Point Label Element model', out__common_label_element, {
    'x': fields.Float(description='Element\'s X position', min=0.0, max=1.0),
    'y': fields.Float(description='Element\'s Y position', min=0.0, max=1.0),
})

out__label_status = api.model('Label status and ID', {
    'label_id': fields.String(description='Label\'s ID', attribute='id'),
    'status': fields.String(description='Status of the label', attribute='status.name'),
})

out__label = api.inherit('Label model', out__label_status, {
    'scan_id': fields.String(description='Scan\'s ID'),
    'elements': fields.List(fields.Polymorph({
        RectangularLabelElement: out__rectangular_label_element,
        BrushLabelElement: out__brush_label_element,
        PointLabelElement: out__point_label_element,
    })),
    'labeling_time': fields.Float(description='Time in seconds that user spent on labeling'),
    'status': fields.String(description='Label\'s status', enum=[status.name for status in LabelVerificationStatus]),
})
