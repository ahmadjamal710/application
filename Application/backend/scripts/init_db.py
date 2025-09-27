#!/usr/bin/env python
"""
Simple database initialization script for Docker
Creates database, runs migrations, and creates a default admin user
"""
import os
import sys
import django
import pymysql
from decouple import config
import time

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_backend.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
import logging

logger = logging.getLogger(__name__)

def wait_for_db():
    """Wait for database to be available"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Test database connection
            connection.ensure_connection()
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            retry_count += 1
            print(f"⏳ Database not ready yet (attempt {retry_count}/{max_retries}). Waiting...")
            time.sleep(2)
    
    print("❌ Failed to connect to database after maximum retries")
    return False

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
        
        print(f"🗄️ Database '{db_name}' created or already exists")
        
        cursor.close()
        connection_obj.close()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        sys.exit(1)

def run_migrations():
    """Run Django migrations"""
    try:
        print("🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'authentication', 'todos'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        sys.exit(1)

def create_admin_user():
    """Create an admin user if it doesn't exist"""
    try:
        from apps.authentication.models import User
        
        if not User.objects.filter(username='admin').exists():
            print("👤 Creating admin user...")
            User.objects.create_user(
                username='admin',
                email='admin@todoapp.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("✅ Admin user created: username=admin, password=admin123")
        else:
            print("ℹ️ Admin user already exists")
    except Exception as e:
        print(f"⚠️ Error creating admin user: {e}")

if __name__ == '__main__':
    print("🚀 Initializing Todo Backend Database...")
    
    if not wait_for_db():
        sys.exit(1)
    
    create_database_if_not_exists()
    run_migrations()
    create_admin_user()
    
    print("🎉 Database initialization completed!")
