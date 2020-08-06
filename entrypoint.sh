#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Migrations
python manage.py makemigrations
python manage.py migrate

# Admin User
python manage.py init_admin

# AWS EC2 Port 80 to 8000
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8000

# Start server
echo "Starting server"
gunicorn AMS.wsgi -b 0.0.0.0:8000
