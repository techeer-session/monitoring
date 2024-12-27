#!/bin/sh

# set two worker for testing purposes. 큐 하나당 워커 하나면 됩니다.

celery -A todo_django worker --loglevel=debug --concurrency=1 -n worker_1_@%h &
celery -A todo_django worker --loglevel=debug --concurrency=1 -n worker_2_@%h &

celery -A todo_django flower --port=5555 --basic_auth=guest:guest --broker=$CELERY_BROKER_URL --broker_api=$CELERY_BROKER_API_URL
