from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import cloudinary.uploader
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
    
    def create(self, validated_data):
     try:
        # Handle image upload with Cloudinary
        if 'image' in validated_data:
            image = validated_data.pop('image')
            upload_response = cloudinary.uploader.upload(image)
            validated_data['image'] = upload_response['url']

        # Pop groups and user_permissions from validated_data
        groups = validated_data.pop('groups', None)  # Extract groups
        user_permissions = validated_data.pop('user_permissions', None)  # Extract user_permissions

        # Create the user object
        user = UserModel(**validated_data)
        if "password" in validated_data:
            validated_data["password"]=user.set_password(validated_data["password"])
        # Set the user as staff if the type is 'Recruiter'
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
