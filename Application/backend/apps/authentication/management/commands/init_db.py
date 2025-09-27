"""
Django management command to initialize the database
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from apps.authentication.models import User


class Command(BaseCommand):
    """Django command to initialize database with migrations and admin user"""
    
    help = 'Initialize database with migrations and create admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-username',
            type=str,
            default='admin',
            help='Admin username (default: admin)'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='admin123',
            help='Admin password (default: admin123)'
        )
        parser.add_argument(
            '--admin-email',
            type=str,
            default='admin@todoapp.com',
            help='Admin email (default: admin@todoapp.com)'
        )

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Initializing database...')
        
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command('makemigrations', 'authentication', verbosity=0)
        call_command('makemigrations', 'todos', verbosity=0)
        call_command('migrate', verbosity=0)
        self.stdout.write(self.style.SUCCESS('Migrations completed'))
        
        # Create admin user
        self.create_admin_user(options)
        
        self.stdout.write(self.style.SUCCESS('Database initialization completed!'))

    def create_admin_user(self, options):
        """Create admin user if it doesn't exist"""
        username = options['admin_username']
        password = options['admin_password']
        email = options['admin_email']
        
        try:
            with transaction.atomic():
                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name='Admin',
                        last_name='User'
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Admin user created: username={username}, password={password}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Admin user "{username}" already exists')
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )
