from django.db import models
from django.contrib.auth.models import *
from cloudinary.models import CloudinaryField
class UserModel(AbstractUser):
     image = CloudinaryField('image', blank=True, null=True)
     mobile_number =models.CharField(max_length=200,null=True, blank=True)
     type =models.CharField(choices=[('Recuiter','Recuiter'),('Student','Student')] ,max_length=50 ,null=True, blank=True)
     def __str__(self):
         return self.first_name
     
class Company(models.Model):
    company_name= models.CharField(max_length=200,null=True,blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company_address=models.TextField(null=True,blank=True)
class Job(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name="user_job")
    company=models.ForeignKey(Company, on_delete=models.CASCADE,related_name="job_company")
    postition=models.CharField(max_length=200,null=True, blank=True)
    job_title=models.CharField(max_length=200,null=True, blank=True)
    job_type=models.CharField(choices=[('Part Time','Part Time') ,('Full Time','Full Time')])
    location =models.CharField(max_length=200,null=True,blank=True)
    salary=models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)