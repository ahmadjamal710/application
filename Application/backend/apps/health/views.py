from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache
import logging
import time

logger = logging.getLogger('todo_backend')

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint to verify app and database status"""
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': time.time(),
            'services': {}
        }
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            health_status['services']['database'] = {
                'status': 'healthy',
                'message': 'Database connection successful'
            }
            logger.info("Health check: Database connection successful")
        except Exception as db_error:
            health_status['services']['database'] = {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(db_error)}'
            }
            health_status['status'] = 'unhealthy'
            logger.error(f"Health check: Database connection failed: {str(db_error)}")
        
        # Check application status
        health_status['services']['application'] = {
            'status': 'healthy',
            'message': 'Application is running'
        }
        
        # Determine overall status
        overall_status = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        
        logger.info(f"Health check completed: {health_status['status']}")
        return Response(health_status, status=overall_status)
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return Response({
            'status': 'unhealthy',
            'timestamp': time.time(),
            'error': 'Internal server error during health check'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
