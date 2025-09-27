#!/bin/bash

echo "Starting Django Todo Backend..."

echo "Waiting for database connection..."
python manage.py wait_for_db --timeout=60

echo "Initializing database..."
python manage.py init_db

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
