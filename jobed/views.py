from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
@login_required
def user_profile(request):
    user = request.user
    return JsonResponse({
        'is_logged_in': 1,
        'username': user.username,
        'profile_photo': user.image.url if hasattr(user, 'image') else '',
        
    })
    
def check_login_status(request):
    if request.user.is_authenticated:
        return Response({'is_logged_in': 1})
    else:
        return Response({'is_logged_in': 0})
    
@api_view(['POST'])
def register(request):
    try:
        data = request.data
        username = data.get('username')
        
        if UserModel.objects.filter(username=username).exists():
            return Response(
                {"message": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Successfully Created", "data": str(serializer.data)},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:   
        return Response(
            {"message": "Something went wrong, please try again", "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return Response({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "type":user.type,
                    "is_logged_in":True
                }
            }, status=200)
        else:
            return Response({'error': 'Invalid Credentials'}, status=400)
    except Exception as e:
        return Response(
            {
                "message":"something went wrong",
                "error":str(e)
            },
            status=400
        )
@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    if request.user.is_authenticated:
        print(request)
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=200)
    return Response({'error': 'User is not logged in'}, status=400)

@api_view(['GET'])
def get_user_data(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            social_account = user.socialaccount_set.get(provider='google')
            extra_data = social_account.extra_data
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'google_data': {
                    'name': extra_data.get('name'),
                    'picture': extra_data.get('picture'),
                    'email': extra_data.get('email'),
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    return Response({'error': 'User not authenticated'}, status=401)
