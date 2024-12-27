# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Set up OpenTelemetry instrumentation (optional)
# RUN pip install opentelemetry-sdk opentelemetry-instrumentation-django opentelemetry-instrumentation-celery opentelemetry-exporter-otlp

# Expose port
EXPOSE 8000

# Command to start the application
CMD ["gunicorn", "todo_project.wsgi:application", "--bind", "0.0.0.0:8000"]
