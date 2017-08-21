"""Module responsible for storage of serializers used in Core endpoints"""
from flask_restplus import fields

from data_labeling.api import api


status = api.model('Status model', {
    'success': fields.Boolean(description='Should be True if everything is all right.'),
})
