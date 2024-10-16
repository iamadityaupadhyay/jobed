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
        data =request.data
        email=data.get('email')
        # now checking that if the user exists or not in our data base
        if UserModel.objects.filter(email=email).exists():
            return Response(
                {"message":"User already exists please register with a different email"},
                status = status.HTTP_406_NOT_ACCEPTABLE
                
            )
        
        # not storing the data in the database in form of objects 
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(
                {
                    "message":"Successfully registered",
                    "data":serializer.data
                }
                ,
                status=status.HTTP_201_CREATED
            ) 
        else:
            return Response(
                {"message":serializer.errors}
            )
        return Response(
          {"message":"something went wrong"}
        )
# # Login API 
# @api_view()
# def login(request):
#     data= request.data