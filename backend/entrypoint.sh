#!/bin/bash
set -e

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Check if a command was passed
if [ "$1" ]; then
    # If a command was passed, execute it
    exec "$@"
else
    # If no command was passed, start the appropriate server based on the environment
    if [ "$DJANGO_ENVIRONMENT" == "production" ] || [ "$DJANGO_ENVIRONMENT" == "Production" ]; then
        # Start Gunicorn for production
        exec gunicorn config.wsgi:application --bind 0.0.0.0:5000 --workers 3
    else
        # Start Django development server
        exec python manage.py runserver 0.0.0.0:5000
    fi
fi