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
from rest_framework_simplejwt.tokens import RefreshToken


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
                {   "success":True,
                    "message": "Successfully Created", 
                    "data": serializer.data,
                },
               
            )
        return Response(
            {
           "error": serializer.errors,
            "success":False,
            "message": "Something went wrong, please try again"
           }
            )
    except Exception as e:   
        return Response(
            {"message": "Something went wrong, please try again", 
             "error": str(e),
            "success":False
             
             },
        )

@api_view(['POST'])

def login_view(request):
    try:
        data = request.data
        username=data.get("username")
        password=data.get("password")
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            user_object=UserModel.objects.get(username=username)
            serializer=UserSerializer(user_object)
            refresh = RefreshToken.for_user(user)
            return Response(
                {    
                    "message":"Successfully logged in",
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                    "success":True,
                    "user":serializer.data
                }
            )
        else:
            return Response(
                {"message":"Invalid Credentials",
                "success":False
                },
            )
    except UserModel.DoesNotExist:
        return Response(
            {"message": "User does not exist",
             "success": False
            },
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"message":"Something went wrong, please try again", 
             "error":str(e),
             "success":False
            }, 
        )   
@api_view(['POST'])
def logout_view(request):
    try:
        refresh = request.data.get('refresh')
        token=RefreshToken(refresh)
        token.blacklist()
        return Response(
            {"message":"Successfully logged out",
             "success":True},
           
        )
    except Exception as e:
        return Response(
            {"message":"Something went wrong, please try again", 
             "success":False,
             "error":str(e)},
           
        )
        

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
