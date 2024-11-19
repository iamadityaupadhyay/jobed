
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import *
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
import jwt
from django.core.exceptions import ObjectDoesNotExist
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
User = get_user_model()

@api_view(['POST'])
def google_login(request):
        
        try:
            credential = request.data.get('credential')
            print(credential)
            request = requests.Request()
            id_info = id_token.verify_oauth2_token(
                credential,
                request,
                '301772127319-m28e15gf0mcpppdvcg9g1drprbdsgtj1.apps.googleusercontent.com'
            )
            print(id_info)
            email = id_info['email']
            name = id_info.get('name', '')
            given_name = id_info.get('given_name', '')
            family_name = id_info.get('family_name', '')
            picture = id_info.get('picture', '')
            
            try:
                user = User.objects.get(email=email)
                user.first_name = given_name
                user.last_name = family_name
                user.image = picture
                user.save()
                
            except ObjectDoesNotExist:
                username = email.split('@')[0]

                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    image =picture,
                    first_name=given_name,
                    last_name=family_name,
        
                    is_active=True
                )
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'image': user.image,
                'type': user.user_type if hasattr(user, 'user_type') else 'Student'
            }
            print(user_data)
            return Response({
                'success': True,
                'token': access_token,
                'user': user_data
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:

            return Response({
                'success': False,
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                 "success":False,
                 "error":str(e)
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
def profile(request,pk):

    try:
        user=get_object_or_404(UserModel,id =pk)
        serializers=UserSerializer(user)
        return Response(
            {
                "message":"Here is the user data",
                "data":serializers.data,
                "success":True
            }
        )
    
    except Exception as e:
        return Response(
            {
                "message":"Bedagark is occuring",
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
@api_view(["PUT"])
def profile_update(request,id):
    if request.method=="PUT":
        data=request.data
        user=get_object_or_404(UserModel,id=id)
        serializer=ProfileSerializer(user,data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message":"Successfully updated",
                    "success":True,
                    "data":serializer.data
                }
            )
        return Response(
            {
                "message":"Something went wrong",
                "success":False,
                "error":serializer.errors
            }
        )
@api_view(['GET'])
def get_profiles(request):
    try:
        
        queryset=UserModel.objects.all()
        serializer = UserSerializer(queryset,many=True)
        print(serializer.data)
        return Response(
            {   
                "data":serializer.data
            }
        )
    except Exception as e:
        return Response(
            {
                "Error":str(e)
            }
        )
@api_view(["GET"])
def get_profile_by_id(request,id):
    #  getting the user first
    response={}
    try:  
        user = get_object_or_404(UserModel, id =id)
        user_s=UserSerializer(user)
    except UserModel.DoesNotExist:
        response['error']=ValueError
    try:
        user_work=user.user_work.all()
        user_projects=user.user_project.all()
        user_education=user.user_education.all()
        user_certificates=user.user_certification.all()
        # calling serializer 
        work_s=WorkExperienceSerializer(user_work,many=True)
        project_s=ProjectsSerializer(user_projects,many=True)
        education_s=EducationSerializer(user_education,many=True)
        certificates_s=CertificationSerializer(user_certificates,many=True)
        response['user']=user_s.data
        response['user_work']=work_s.data
        response['user_projects']=project_s.data
        response['user_education']=education_s.data
        response['user_certificates']=certificates_s.data
        response["success"]=True
        return Response(
        {"data" : response}
    )
    except Exception as e:
        response['exception']=e
    print(response)
    
    
    
# updating skill 
# skill getting working fine
@api_view(["GET"])
def skill_get(request,id):
    try:
        if request.method=="GET":
            user=get_object_or_404(UserModel,id=id)
            skill=get_object_or_404(Skill,user=user)
            serializers=SkillSerializer(skill)
            return Response(
                serializers.data,    
            )
    except Exception as e:
        return Response(
            {"error":str(e)}
        )
@api_view(["PUT"])
def skill_update(request ,id):
    try:
        if request.method=="PUT":
            data=request.data
            print(data)
            # now the data is here now we want to update 
            # calling the serializer
            user = get_object_or_404(UserModel,id=id)
            skill, created = Skill.objects.get_or_create(user=user)
            # in serializer the first parameter is telling which model is to be checked for updating
            serializers = SkillSerializer(skill, data=data, partial=True)
            if serializers.is_valid():
                print("ok")
                serializers.save()
                return Response(
                    {"message":"successfully updated the skills",
                    "data":serializers.data,
                    "success":True
                    
                    }
                )
            else:
                return Response(
                    {
                        "message":"Something went wrong",
                        "error":serializers.errors
                    }
                )
    except Exception as e:
        return Response(
           { "error":str(e)}
        )  
@api_view(["PUT"])  
def about_update(request,id):
    if request.method=="PUT":
        try:
            data=request.data
            # now we have the data in json format 
            # calling the serializer
            print(data) 
            user = get_object_or_404(UserModel,id=id)
            about, created = About.objects.get_or_create(user=user)
            # in serializer the first parameter is telling which model is to be checked for updating
            serializers = AboutSerializer(about, data=data, partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response(
                {
                    "message":"Successfully updated",
                    "success":True,
                    "data":serializers.data
                }
            )
            else:
                return Response(
                    {
                        "error":serializers.errors
                    }
                )
        except Exception as e:
            return Response (
                {
                    "message":"some error occured",
                    "success":False,
                    "error":str(e)
                }
            )
@api_view(["GET"])
def about_get(request, id):
    try:
        if request.method=="GET":
            user= get_object_or_404(UserModel,id=id)
            about = About.objects.get(user=user)
            serializers=AboutSerializer(about)
            return Response(
                {
                    "message":"successfully retrieved",
                    "data":serializers.data,
                    "success":True
                }
            )
          
    except Exception as e:
        return Response(
            {
                "message":"some error occured",
                "error":str(e)
            }
        )
@api_view(['PUT'])
def education_update(request,id):
    try:
        if request.method=="PUT":
            data=request.data
            print(data)
            user=get_object_or_404(UserModel,id=id)
            # {'education': [{'college_name': 'Goel ', 'college_address': 'Lucknow', 'percentage': '9'}, 
            # {'college_name': 'Gitm', 'college_address': 'lko', 'percentage': '9'}]}
            education_response=[]
            for education in data.get('education',[]):
                edu_id=education.get("id")
                if edu_id:
                        education_instance=Education.objects.get(id=edu_id)
                        serializers=EducationSerializer(education_instance,data=education,partial=True)
                else:
                    # if there is not in model 
                    serializers = EducationSerializer(data={**education, "user": user.id})
                if serializers.is_valid():
                    serializers.save()
                    education_response.append(serializers.data)
            return Response(
                {
                    "message":"successfull",
                    "data":education_response
                    
                },
                
            )
    except Exception as e:
        return Response(
            {
                "message":"something is wrong",
                "error":str(e)
            }
        )
@api_view(['PUT'])
def experience_update(request,id):
    try:
        if request.method=="PUT":
            data=request.data
            # now we have the data 
            print(data)
            user=get_object_or_404(UserModel,id=id)
            experience_response=[]
            error=[]
            # now we have so many experiences in the data fiels
            for exp in data.get("experience",[]):
                exp_id=exp.get("id")
                
                if exp_id:
                    # it represents that we have the experience 
                    # now updating 
                    exp_instance= WorkExperience.objects.get(id=exp_id)
                    print(exp_id)
                    serializers= WorkExperienceSerializer(exp_instance,data=exp,partial=True)
                else:
                    # it means we dont have the exp in workexp table
                    serializers=WorkExperienceSerializer(data={**exp, "user": user.id})
                    print("here")
                if serializers.is_valid():
                    serializers.save()
                    experience_response.append(serializers.data)
                else:
                    error.append(serializers.errors)
                    print(error)
            return Response(
                    {
                        "message":"successfully updated",
                        "data":serializers.data 
                    },
                
                )
    except Exception as e:
        return Response(
            {
                "message":"something is not going smooth",
                "error":str(e)
            }
        )