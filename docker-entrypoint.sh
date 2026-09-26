#!/bin/sh
set -eu
python manage.py migrate --noinput
python manage.py seed_demo
python manage.py setup_demo_admin
exec gunicorn folp.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 1 \
  --threads 2 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
