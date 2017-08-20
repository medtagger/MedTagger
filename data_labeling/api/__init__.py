"""Module responsible for defining API"""
from flask import Blueprint
from flask_restplus import Api


# Definition of the API
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='0.1', title='Backend API', description='Documentation for Backend API')
