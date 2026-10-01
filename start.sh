#!/usr/bin/env bash
set -e

# Celery worker in the background (low memory)
celery -A yourproject worker --loglevel=info --pool=solo &

# Gunicorn in the foreground, bound to Render's port
exec gunicorn yourproject.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 1 \
  --timeout 120