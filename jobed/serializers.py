from rest_framework import serializers
from .models import *
# from django auth headers import make_password

from django.contrib.auth.hashers import make_password
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields="__all__"
        
    # overwriting create function to overwrite it and hash the password it means the data which cames from the frontend after call the serializer then it will go through the create 
    def create(self, validated_data):
        validated_data['password']=make_password(validated_data['password'])
        return super(UserSerializer,self).create(validated_data)    