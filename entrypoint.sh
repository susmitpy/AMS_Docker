#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput


# AWS EC2 Port 80 to 8000
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8000

# Start server
echo "Starting server"
gunicorn ams.wsgi -b 0.0.0.0:8000
