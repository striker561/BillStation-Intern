#!/bin/sh
set -e

if [ -n "$DATABASE_URL" ]; then
  echo "DATABASE_URL provided"
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

exec gunicorn auth_service.wsgi:application --bind 0.0.0.0:8000
