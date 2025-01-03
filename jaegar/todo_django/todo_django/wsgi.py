"""
WSGI config for todo_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from opentelemetry.instrumentation.django import DjangoInstrumentor
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_django.settings')
DjangoInstrumentor().instrument()
application = get_wsgi_application()
