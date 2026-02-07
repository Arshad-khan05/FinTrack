#!/usr/bin/env bash
set -e

# Run DB migrations and collect static files before starting the app
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn binding to the Render-provided port (use python -m to avoid PATH issues)
exec python -m gunicorn FinTrack.wsgi:application --bind 0.0.0.0:$PORT
