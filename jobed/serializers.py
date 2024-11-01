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
    