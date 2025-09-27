from django.urls import path
from . import views

urlpatterns = [
    path('', views.todos_list_create, name='todos_list_create'),  # GET for list, POST for create
    path('<int:todo_id>/', views.todo_detail, name='todo_detail'),  # GET, PUT, DELETE for specific todo
]
