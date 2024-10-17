from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view
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


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request,username=username, password=password)
    
    if user is not None:
        login(request,user)
        return Response(
            {"message":"login successfull" ,"data":user},
            status=200
        )
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
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    else:
        return Response({'error': 'User not authenticated'}, status=401)