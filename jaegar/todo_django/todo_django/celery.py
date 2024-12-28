import os
from celery import Celery
from django.conf import settings
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_django.settings')

TRACING_EXPORTER_ENDPOINT = os.environ.get('JAEGER_ENDPOINT', 'http://127.0.0.1:4317')

resource = Resource(attributes={
  SERVICE_NAME: "celery-worker"
})

traceProvider = TracerProvider(resource=resource)

TRACING_EXPORTER_ENDPOINT = os.environ.get('JAEGER_ENDPOINT', TRACING_EXPORTER_ENDPOINT)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=TRACING_EXPORTER_ENDPOINT))
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

tracer = trace.get_tracer(__name__)

app = Celery('todo_django', broker='amqp://guest:guest@rabbitmq//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)