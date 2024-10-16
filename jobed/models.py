from django.db import models
from django.contrib.auth.models import *
from cloudinary.models import CloudinaryField
class UserModel(AbstractUser):
     image = CloudinaryField('image',null=True ,blank=True)
     
     mobile_number =models.IntegerField()
     type =models.CharField(choices=[('Recuiter','Recuiter'),('Student','Student')] ,max_length=50 ,null=True, blank=True)
     def __str__(self):
         return self.first_name
    