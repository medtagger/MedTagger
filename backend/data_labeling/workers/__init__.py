"""Module responsible for defining Celery application"""
from celery import Celery


celery_app = Celery('data_labeling')
celery_app.config_from_object('data_labeling.workers.celery_configuration')
