from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import cloudinary.uploader
from .models import *



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields="__all__"
    def create(self, validated_data):
        try:
            # Check if the 'image' field is in the validated data
            if 'image' in validated_data:
                image = validated_data.pop('image')  # Pop the image out of the validated data
                # Upload the image to Cloudinary
                upload_response = cloudinary.uploader.upload(image)
                # Get the URL from the response and set it in the validated data
                validated_data['image'] = upload_response['url']
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
        return super().create(validated_data)
class JobSerializer(serializers.ModelSerializer):
    company=CompanySerializer()
    class Meta:
        model=Job
        fields="__all__"
    def create(self, validated_data):
        try:
            # Check if the 'image' field is in the validated data
            if 'image' in validated_data:
                image = validated_data.pop('image')  # Pop the image out of the validated data
                # Upload the image to Cloudinary
                upload_response = cloudinary.uploader.upload(image)
                # Get the URL from the response and set it in the validated data
                validated_data['image'] = upload_response['url']
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
        return super().create(validated_data)
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        fields="__all__"
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Education
        fields="__all__"
class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model=WorkExperience
        fields="__all__"
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Certification
        fields="__all__"
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Projects
        fields="__all__"
class UserSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = UserModel
        fields = "__all__"
    
    def create(self, validated_data):
     try:
        if 'image' in validated_data:
            image = validated_data.pop('image')
            upload_response = cloudinary.uploader.upload(image)
            validated_data['image'] = upload_response['url']

        groups = validated_data.pop('groups', None) 
        user_permissions = validated_data.pop('user_permissions', None)

        user = UserModel(**validated_data)
        if "password" in validated_data:
            validated_data["password"]=user.set_password(validated_data["password"])
        if validated_data['type'] == 'Recruiter':
            user.is_staff = True
            user.is_active=True
        user.save()
        if groups is not None:
            user.groups.set(groups) 
        if user_permissions is not None:
            user.user_permissions.set(user_permissions)
        return user
     except Exception as e:
        raise serializers.ValidationError(f"Error creating user: {str(e)}")
    def update(self, instance, validated_data):
        try:
            if 'image' in validated_data:
                image = validated_data.pop('image')
                upload_response = cloudinary.uploader.upload(image)
                validated_data['image'] = upload_response['url']
        except Exception as e:
            print(f"Error uploading image: {str(e)}")
        return super().update(instance, validated_data)
class ProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, source='user_education', required=False)
    work_experience = WorkExperienceSerializer(many=True, source='user_work', required=False)
    projects=ProjectsSerializer(many=True,required=False,source="user_project")
    certificates= CertificationSerializer(many=True, required=False, source= "user_certification")
    
    class Meta:
        model = UserModel
        fields = "__all__"

    def update(self, instance, validated_data):
        education_data = validated_data.pop('user_education', [])
        work_experience_data = validated_data.pop('user_work', [])
        projects_data= validated_data.pop('user_project',[])
        cerificate_data=validated_data.pop('user_certificate',[])

        for edu_item in education_data:
            edu_id = edu_item.pop('id', None)
            if edu_id is not None:
            # updating
                edu_instance = instance.user_education.get(id=edu_id)
                edu_serializer = EducationSerializer(edu_instance, data=edu_item, partial=True)
            else:
            # if not exists 
                edu_item['user'] = instance.id
                edu_serializer = EducationSerializer(data=edu_item)

            if edu_serializer.is_valid(raise_exception=True):
                edu_serializer.save()

        for work_item in work_experience_data:
            work_id = work_item.pop('id', None)
            if work_id is not None:
                work_instance = instance.user_work.get(id=work_id)
                work_serializer = WorkExperienceSerializer(work_instance, data=work_item, partial=True)
            else:
                work_item['user'] = instance.id
                work_serializer = WorkExperienceSerializer(data=work_item)

            if work_serializer.is_valid(raise_exception=True):
                work_serializer.save()
        #  now getting the projects of the user 
        # getting all the data by first popping the data from the validated 
        for project in projects_data:
            project_id = project.pop("id",None)
            # updating if exists
            if project_id is not None:
                try:
                    project_instance = instance.user_project.get(id=project_id)
                except Exception as e :
                    print(e)
                project_serializer = ProjectsSerializer(project_instance, data = project,partial=True)
            # creating if not present 
            else :
                project['user']=instance.id
                project_serializer = ProjectsSerializer(data = project)
            if project_serializer.is_valid(raise_exception=True):
                project_serializer.save()
        # handling certificates
        for c in cerificate_data:
            if c:
                c_id= c.pop("id",None)
                if c_id is not None:
                    try:
                        c_instance = instance.user_certification.get(id=c_id)
                    except Exception as e:
                        print(e)
                     # updating if exists
                    c_serializer= CertificationSerializer(c_instance, data=c)
                #  creating new if not 
                
                else:
                    c_serializer=CertificationSerializer(data=c)
                if c_serializer.is_valid(raise_exception=True):
                    c_serializer.save()
                    
        return super().update(instance, validated_data)
class SkillSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Skill
        fields="__all__"
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
class InterestSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Interest
        fields="__all__"
class AboutSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=About
        fields="__all__"
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)