"""
Django management command to wait for database to be available
"""
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available"""
    
    help = 'Wait for database to be available'

    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout',
            type=int,
            default=60,
            help='Maximum time to wait for database (seconds)'
        )

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        
        timeout = options['timeout']
        start_time = time.time()
        
        while True:
            try:
                # Test database connection
                db_conn = connections['default']
                db_conn.cursor()
                break
            except OperationalError:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    self.stdout.write(
                        self.style.ERROR(f'Database unavailable after {timeout} seconds')
                    )
                    raise
                
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
