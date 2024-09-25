#!/bin/bash
set -e

# Apply database migrations
python manage.py migrate

# Start the Django application
if [ "$DJANGO_DEBUG" = "False" ]; then
    # Start Gunicorn for production
    gunicorn config.wsgi:application --bind 0.0.0.0:5000 --workers 3
else
    # Start Django development server
    python manage.py runserver 0.0.0.0:5000
fi