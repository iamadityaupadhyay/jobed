from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.decorators import *
from rest_framework.response import Response
# Create your views here.
from rest_framework.decorators import *
from rest_framework.status import *
from .serializers import *
# Login API 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login , logout
from django.contrib.auth.decorators import *

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@api_view(['POST'])
def register(request):
   
    # the data will come from frontend in the form of json
    try:
        data =request.data
        username=data.get('username')
        # now checking that if the user exists or not in our data base
        
        if UserModel.objects.filter(username=username).exists():
            return Response(
                {"message":"User is already exists"},
                status = status.HTTP_400_BAD_REQUEST
                
            )
        
        # not storing the data in the database in form of objects 
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(
                {"message":"Successfully Created",
                 "data":serializer.data
                },
                status=status.HTTP_201_CREATED
            ) 
    except:   
        return Response(
            {"message":"Something went wrong please try again"},
          status=status.HTTP_400_BAD_REQUEST
        )

from django.views.decorators.http import require_GET

@method_decorator(csrf_exempt, name='dispatch')
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, status=200)
    else:
        return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)
@api_view(['GET'])
def user_profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        serializer=UserSerializer(user)
        return Response({
            "data":serializer.data,
            "message":"The requested user data is"
        })
    else:
        return Response({'error': 'User not authenticated'}, status=401)
    
@require_GET
@login_required
def get_user_data(request):
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