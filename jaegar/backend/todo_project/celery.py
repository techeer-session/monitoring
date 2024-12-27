from celery import Celery

app = Celery("todo_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
