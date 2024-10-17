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
            if 'image' in validated_data:
                image = validated_data.pop('image')
                upload_response = cloudinary.uploader.upload(image)
                validated_data['image'] = upload_response['url']
        except Exception as e:
            raise serializers.ValidationError({"image": "Failed to upload image to Cloudinary."})
        
        # Handle many-to-many fields (if any)
        groups = validated_data.pop('groups', None)
        permissions = validated_data.pop('user_permissions', None)
        
        password = validated_data.pop('password', None)
        if password:
            user = UserModel(**validated_data)
            user.set_password(password)
            user.save()

            # Now add the many-to-many relationships using set()
            if groups:
                user.groups.set(groups)
            if permissions:
                user.user_permissions.set(permissions)

            return user
        else:
            raise serializers.ValidationError({"password": "Password is required."})
