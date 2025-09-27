#!/bin/bash

# Start server script for development
echo "Starting Django Todo Backend Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python scripts/init_database.py

# Start the server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
