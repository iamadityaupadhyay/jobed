from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import cloudinary.uploader
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
    
    def create(self, validated_data):
        
        if 'image' in validated_data:
            print('image')
            image = validated_data.pop('image')
            upload_response = cloudinary.uploader.upload(image)
            validated_data['image'] = upload_response['url']
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user
