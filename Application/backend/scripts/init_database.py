#!/usr/bin/env python
"""
Database initialization script
Run this script to create the database and apply migrations
"""
import os
import sys
import django
import pymysql
from decouple import config

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_backend.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
import logging

logger = logging.getLogger(__name__)

def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server without specifying database
        db_config = {
            'host': config('DB_HOST', default='localhost'),
            'port': int(config('DB_PORT', default='3306')),
            'user': config('DB_USER', default='root'),
            'password': config('DB_PASSWORD', default='password'),
        }
        
        connection_obj = pymysql.connect(**db_config)
        cursor = connection_obj.cursor()
        
        db_name = config('DB_NAME', default='todoapp')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        print(f"Database '{db_name}' created or already exists")
        
        cursor.close()
        connection_obj.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

def run_migrations():
    """Run Django migrations"""
    try:
        print("Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("Migrations completed successfully")
    except Exception as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)

def create_superuser():
    """Create a superuser if it doesn't exist"""
    try:
        from apps.authentication.models import User
        
        if not User.objects.filter(is_superuser=True).exists():
            print("Creating superuser...")
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("Superuser created: username=admin, password=admin123")
        else:
            print("Superuser already exists")
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == '__main__':
    print("Initializing database...")
    create_database_if_not_exists()
    run_migrations()
    create_superuser()
    print("Database initialization completed!")
