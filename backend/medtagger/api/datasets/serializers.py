"""Module responsible for storage of serializers used in Datasets endpoints."""
from flask_restplus import fields

from medtagger.api import api
from medtagger.api.tasks.serializers import out__task

in__dataset = api.model('New Dataset model', {
    'key': fields.String(),
    'name': fields.String(),
})

out__dataset = api.model('Dataset model', {
    'key': fields.String(),
    'name': fields.String(),
    'tasks': fields.List(fields.Nested(out__task)),
})
