from app.tasks import celery_app

# This file is required to run the worker with:
# celery -A app.celery_worker worker --loglevel=info