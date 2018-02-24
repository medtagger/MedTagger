"""Module responsible for defining Celery application."""
from celery import Celery


celery_app = Celery('medtagger')
celery_app.config_from_object('medtagger.workers.celery_configuration')
celery_app.log.setup()
