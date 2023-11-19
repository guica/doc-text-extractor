from doc_analyser import settings


class Config:
    CELERY_BROKER_URL = settings.CELERY_BROKER_URL
    CELERY_BACKEND = settings.CELERY_BACKEND
    imports = ("doc_analyser.tasks",)
    result_expires = 60 * 15
    timzone = "America/Sao_Paulo"

    accept_content = ["json", "msgpack", "yaml"]
    task_serializer = "json"
    result_serializer = "json"

    task_routes = {
        "doc_analyser.tasks.convert_file_to_text": {
            "queue": "default"
        },
        "doc_analyser.tasks.convert_to_pdf": {
            "queue": "pdf"
        },
        "doc_analyser.tasks.get_keywords_from_text": {
            "queue": "default"
        },
    }
