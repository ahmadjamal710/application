from django.http import JsonResponse

def api_endpoints(request):
    """
    Root endpoint that lists all available API endpoints
    """
    endpoints = {
        "message": "Todo List API - Available Endpoints",
        "endpoints": {
            "health": {
                "url": "/health/",
                "method": "GET",
                "description": "App health and database connection status"
            },
            "auth": {
                "register": {
                    "url": "/auth/register/",
                    "method": "POST",
                    "description": "User registration"
                },
                "login": {
                    "url": "/auth/login/", 
                    "method": "POST",
                    "description": "User login"
                },
                "logout": {
                    "url": "/auth/logout/",
                    "method": "POST", 
                    "description": "User logout"
                }
            },
            "todos": {
                "list": {
                    "url": "/todos/",
                    "method": "GET",
                    "description": "List user's todos"
                },
                "create": {
                    "url": "/todos/",
                    "method": "POST",
                    "description": "Create new todo"
                },
                "update": {
                    "url": "/todos/{id}/",
                    "method": "PUT",
                    "description": "Update todo"
                },
                "delete": {
                    "url": "/todos/{id}/",
                    "method": "DELETE",
                    "description": "Delete todo"
                }
            }
        }
    }
    return JsonResponse(endpoints, json_dumps_params={'indent': 2})
