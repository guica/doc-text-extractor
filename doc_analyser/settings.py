from os import environ

CATEGORIZER_API_URL = environ.get('CATEGORIZER_INTERNAL_IP') + '/api/v1/document/'
CATEGORIZER_API_AUTH_TOKEN = environ.get('AUTH_TOKEN')

DOC_PREVIEW_PATH = '/output_files/preview/'
FULL_DOCS_PATH = '/output_files/full_docs/'

CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
CELERY_BACKEND = environ.get('CELERY_BACKEND')