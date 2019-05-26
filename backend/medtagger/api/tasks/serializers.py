"""Module responsible for storage of serializers used in Tasks endpoints."""
from flask_restplus import fields

from medtagger.api import api
from medtagger.definitions import LabelTool

out__label_tag = api.model('Label Tag model', {
    'key': fields.String(),
    'name': fields.String(),
    'actions_ids': fields.List(fields.Integer(),
                               attribute=lambda label_tag: [action.id for action in label_tag.actions]),
    'tools': fields.List(fields.String(), description='Available tools for Label Tag',
                         enum=[tool.name for tool in LabelTool],
                         attribute=lambda label_tag: [tool.name for tool in label_tag.tools]),
})

in__label_tag = api.model('Label Tag model', {
    'key': fields.String(),
    'name': fields.String(),
    'actions_ids': fields.List(fields.Integer()),
    'tools': fields.List(fields.String(), description='Available tools for Label Tag',
                         enum=[tool.name for tool in LabelTool]),
})

out__task = api.model('Task model', {
    'key': fields.String(),
    'name': fields.String(),
    'image_path': fields.String(),
    'tags': fields.List(fields.Nested(out__label_tag), attribute=lambda task: sorted(task.available_tags,
                                                                                     key=lambda tag: tag.name)),
    'number_of_available_scans': fields.Integer(),
    'description': fields.String(required=False),
    'label_examples': fields.List(fields.String(), required=False),
    'datasets_keys': fields.List(fields.String(), attribute=lambda task: [dataset.key for dataset in task.datasets]),
})

in__task = api.model('New Task model', {
    'key': fields.String(),
    'name': fields.String(),
    'image_path': fields.String(),
    'datasets_keys': fields.List(fields.String()),
    'description': fields.String(required=False),
    'label_examples': fields.List(fields.String(), required=False),
    'tags': fields.List(fields.Nested(in__label_tag), attribute='available_tags'),
})
