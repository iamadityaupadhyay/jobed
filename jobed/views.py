from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from rest_framework.decorators import *
from rest_framework.status import *
from .serializers import *
@api_view(['POST'])
def register(request):
   
    # the data will come from frontend in the form of json
    try:
        data =request.data
        email=data.get('email')
        # now checking that if the user exists or not in our data base
        if UserModel.objects.filter(email=email).exists():
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
          status=status.HTTP_400_BAD_REQUEST
        )
# Login API 
@api_view()
def login(request):
    # the data which came from frontend
    
    data= request.data