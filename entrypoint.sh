#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Migrations
python manage.py makemigrations
python manage.py migrate

# Admin User
python manage.py init_admin

# Start server
echo "Starting server"
gunicorn AMS.wsgi -b 0.0.0.0:8000 
