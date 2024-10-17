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
            
            return super(UserSerializer, self).create(validated_data)
        
        except Exception as e:
            raise e