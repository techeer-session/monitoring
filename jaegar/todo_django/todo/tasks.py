from celery import shared_task
from todo_django.celery import app
import time

@app.task()
def add_with_delay(x, y):
    time.sleep(2)
    return x + y