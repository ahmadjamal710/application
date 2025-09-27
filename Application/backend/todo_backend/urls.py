from django.contrib import admin
from django.urls import path, include
from .views import api_endpoints

urlpatterns = [
    path('', api_endpoints, name='api_endpoints'),
    path('admin/', admin.site.urls),
    path('health/', include('apps.health.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('todos/', include('apps.todos.urls')),
]
