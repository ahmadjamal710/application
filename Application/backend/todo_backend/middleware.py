import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('todo_backend')

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        logger.info(f"Request started: {request.method} {request.path}")
        return None

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"Request completed: {request.method} {request.path} "
                f"Status: {response.status_code} Duration: {duration:.3f}s"
            )
        return response

    def process_exception(self, request, exception):
        logger.error(f"Request error: {request.method} {request.path} Error: {str(exception)}")
        return None
