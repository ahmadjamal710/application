from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

from .models import Todo
from .serializers import TodoSerializer, TodoCreateSerializer, TodoUpdateSerializer
from apps.authentication.models import User

logger = logging.getLogger('todo_backend')

def get_authenticated_user(request):
    """Get authenticated user from session"""
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@method_decorator(csrf_exempt)
def todos_list_create(request):
    """List all todos or create a new todo for the authenticated user"""
    user = get_authenticated_user(request)
    if not user:
        return Response({
            'error': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        try:
            todos = Todo.objects.filter(user_id=user.id)
            serializer = TodoSerializer(todos, many=True)
            logger.info(f"Listed {len(todos)} todos for user: {user.username}")
            return Response({
                'todos': serializer.data,
                'count': len(todos)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error listing todos for user {user.username}: {str(e)}")
            return Response({
                'error': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            serializer = TodoCreateSerializer(data=request.data)
            if serializer.is_valid():
                todo = serializer.save(user_id=user.id)
                logger.info(f"Created todo '{todo.title}' for user: {user.username}")
                return Response({
                    'message': 'Todo created successfully',
                    'todo': TodoSerializer(todo).data
                }, status=status.HTTP_201_CREATED)
            
            logger.warning(f"Todo creation failed for user {user.username}: {serializer.errors}")
            return Response({
                'error': 'Todo creation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error creating todo for user {user.username}: {str(e)}")
            return Response({
                'error': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
@method_decorator(csrf_exempt)
def todo_detail(request, todo_id):
    """Retrieve, update or delete a specific todo for the authenticated user"""
    user = get_authenticated_user(request)
    if not user:
        return Response({
            'error': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        todo = get_object_or_404(Todo, id=todo_id, user_id=user.id)
    except:
        logger.warning(f"Todo {todo_id} not found for user: {user.username}")
        return Response({
            'error': 'Todo not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        try:
            serializer = TodoSerializer(todo)
            logger.info(f"Retrieved todo '{todo.title}' for user: {user.username}")
            return Response({
                'todo': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving todo {todo_id} for user {user.username}: {str(e)}")
            return Response({
                'error': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            serializer = TodoUpdateSerializer(todo, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_todo = serializer.save()
                logger.info(f"Updated todo '{updated_todo.title}' for user: {user.username}")
                return Response({
                    'message': 'Todo updated successfully',
                    'todo': TodoSerializer(updated_todo).data
                }, status=status.HTTP_200_OK)
            
            logger.warning(f"Todo update failed for user {user.username}: {serializer.errors}")
            return Response({
                'error': 'Todo update failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error updating todo {todo_id} for user {user.username}: {str(e)}")
            return Response({
                'error': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        try:
            todo_title = todo.title
            todo.delete()
            logger.info(f"Deleted todo '{todo_title}' for user: {user.username}")
            return Response({
                'message': 'Todo deleted successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error deleting todo {todo_id} for user {user.username}: {str(e)}")
            return Response({
                'error': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
