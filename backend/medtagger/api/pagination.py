"""Module that contains helpers related to pagination in the REST API."""
from flask_restplus import fields

from medtagger.api import api


PAGINATION = {
    'pagination': fields.Nested(api.model('Pagination', {
        'page': fields.Integer(description='Page number'),
        'per_page': fields.Integer(description='Number of entries per page'),
        'total': fields.Integer(description='Total numer of entries'),
    })),
}
