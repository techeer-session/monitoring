import time
import random
from celery import shared_task
from opentelemetry.instrumentation.celery import CeleryInstrumentor
CeleryInstrumentor().instrument()

@shared_task
def generate_random_number():
    time.sleep(2)
    return random.randint(1, 100)
