
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import *
@api_view(['POST'])
def register(request):
    try:
        data = request.data
        username = data.get('username')
        type=data.get("type")
        
        if UserModel.objects.filter(username=username).exists():
            return Response(
                {"message": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(
                {   "success":True,
                    "message": "Successfully Created", 
                    "user": serializer.data,
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
# from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
@api_view(['POST'])

def login_view(request):
    try:
        data = request.data
        username=data.get("username")
        password=data.get("password")
      
        try :
           user = get_user_model().objects.get(username=username)
           if user:
                serializer=UserSerializer(user)
                if user.check_password(password):
                    print("True")
                    refresh = RefreshToken.for_user(user)
                    return Response(
                    {    
                        "message":"Successfully logged in",
                        "refresh":str(refresh),
                        "access":str(refresh.access_token),
                        "success":True,
                        "user":serializer.data,
                        
                    }
                )
                else:
                    return Response(
                        {"message":"Invalid Credentials",
                        "success":False
                        },
                    )
        except Exception as e:
            return Response(
                {"message":"Something went wrong, please try again",
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
        except user.socialaccount_set.model.DoesNotExist:
           
            return Response({'error': 'No Google account linked'}, status=400)
        except Exception as e:

            return Response({'error': f'An error occurred: {str(e)}'}, status=400)


def profile(request,pk):
    try:
     if request.user.is_authenticated:
        user=get_object_or_404(UserModel,id =pk)
        serializers=UserSerializer(data=user)
        return Response(
            {
                "message":"Here is the user data",
                "data":serializers.data,
                "success":True
            }
        )
     else:
         return Response(
             {
                 "message":"Something went wrong",
                 "error":str(serializers.error),
                 "success":False,
             }
         )
    except Exception as e:
        return Response(
            {
                "message":"Someanother error is occuring",
                "success":False,
                "error":str(e)
            }
        )
    
    
# Companies 
from rest_framework.views import APIView
@api_view(["GET"])
def get_companies(request):
        companies= Company.objects.all()
        # using serializer to convert the data into json
        serializer = CompanySerializer(companies,many=True)
        return Response(
            {
                "message":"Here is all the companies",
                "success":"True",
                "comapnies":serializer.data
            }
        )
@api_view(["GET"])
def get_company_by_id(request,id):
    try:
        
        company = get_object_or_404(Company,id=id)
        
        serializers=CompanySerializer(company)
        return Response(
            {
                "message":"Here is the requested objects",
                "success":True,
                "company":serializers.data
            }
        )
    except Exception as e:
        return Response(
            {
                "message":"Sorry something went wrong",
                "error":str(e),
                "success":False
            }
        )
@api_view(['GET'])
def get_job(request):
    try:
        job=Job.objects.all()
        serializers=JobSerializer(job,many=True)
 
        print(serializers.data)
       
        return Response(
            {
                "message":"Here is all the data",
                "success":True,
                "jobs":serializers.data,

            }
        )
    except Exception as e:
        return Response(
            {
                "message":"Something went wrong",
                "error":str(e)
            }
        )
@api_view(["GET"])   
def get_job_by_id(request,id):
    try:
        jobs=get_object_or_404(Job,id=id)
        serializers=JobSerializer(jobs)
        return Response(
            {
                "message":"Here is the data",
                "success":True,
                "job":serializers.data
            }
        )
    except Exception as e:
        return Response(
            {
                "message":"Something went wrong",
                "error":str(e)
            }
        )
        
def applied_jobs(request, id):
    job = get_object_or_404(Job,user=id)
    serializers=JobSerializer(job,many=True)
    return Response(
        {
            "message":"Here is all the data",
            "success":True,
            "job":serializers.data
        }
    )
