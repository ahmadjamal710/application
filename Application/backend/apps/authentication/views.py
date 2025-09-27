from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .models import User

logger = logging.getLogger('todo_backend')

@api_view(['POST'])
@permission_classes([AllowAny])
@method_decorator(csrf_exempt)
def register_view(request):
    """User registration endpoint"""
    try:
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"New user registered: {user.username}")
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Registration failed: {serializer.errors}")
        return Response({
            'error': 'Registration failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@method_decorator(csrf_exempt)
def login_view(request):
    """User login endpoint"""
    try:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Store user ID in session for simple authentication
            request.session['user_id'] = user.id
            logger.info(f"User logged in: {user.username}")
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        logger.warning(f"Login failed: {serializer.errors}")
        return Response({
            'error': 'Login failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@method_decorator(csrf_exempt)
def logout_view(request):
    """User logout endpoint"""
    try:
        user_id = request.session.get('user_id')
        username = 'Anonymous'
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                username = user.username
            except User.DoesNotExist:
                pass
        
        request.session.flush()
        logger.info(f"User logged out: {username}")
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
