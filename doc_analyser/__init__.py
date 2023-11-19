from celery import Celery

from doc_analyser.celery_config import Config
from flask import Flask, request, jsonify

app = Flask(__name__)

celery = Celery(app.import_name, backend=Config.CELERY_BACKEND, broker=Config.CELERY_BROKER_URL)
celery.config_from_object(Config)

TaskBase = celery.Task

class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

celery.Task = ContextTask

# TaskBase = celery.Task

# class ContextTask(TaskBase):
#     abstract = True

#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return TaskBase.__call__(self, *args, **kwargs)

# celery.Task = ContextTask
