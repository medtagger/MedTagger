"""Module responsible for storage of serializers used in Core endpoints."""
from flask_restplus import fields

from medtagger.api import api


out__status = api.model('Status model', {
    'success': fields.Boolean(description='Should be True if everything is all right.'),
})
