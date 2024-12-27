from celery import shared_task
from todo_django.celery import app
import time
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry import trace



tracer = trace.get_tracer(__name__)
@shared_task
def add_with_delay(x, y, title, headers):
    ctx = TraceContextTextMapPropagator().extract(carrier=headers)
    with tracer.start_as_current_span('셀러리 스팬', context=ctx):
        span = trace.get_current_span()
        span.set_attribute("title", title)
        time.sleep(10)
    return x + y