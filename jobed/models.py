from django.db import models
from django.contrib.auth.models import *
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
class UserModel(AbstractUser):
     USER_TYPE_CHOICES = [
        ('Recruiter', 'Recruiter'),
        ('Student', 'Student'),
    ]
     image = CloudinaryField('image', blank=True, null=True)
     mobile_number =models.CharField(max_length=200,null=True, blank=True)
     type =models.CharField(choices=USER_TYPE_CHOICES ,max_length=50 ,null=True, blank=True)
     groups = models.ManyToManyField(Group, blank=True)
     def __str__(self):
         return self.first_name
    

class Company(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True, blank=True)
    company_name= models.CharField(max_length=200,null=True,blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company_address=models.TextField(null=True,blank=True)
    slug =models.SlugField(max_length=400,null=True,blank=True)
    def save(self, *args,**kwrgs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        return super(Company,self).save(*args,**kwrgs)
    def __str__(self):
        return self.company_name
class Job(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name="user_job")
    company=models.ForeignKey(Company, on_delete=models.CASCADE,related_name="job_company")
    postition=models.CharField(max_length=200,null=True, blank=True)
    job_title=models.CharField(max_length=200,null=True, blank=True)
    job_type=models.CharField(choices=[('Part Time','Part Time') ,('Full Time','Full Time')])
    location =models.CharField(max_length=200,null=True,blank=True)
    salary=models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug =models.SlugField(max_length=400, null=True,blank=True)
    job_description=models.TextField(null=True,blank=True)
    job_requirement=models.TextField(null=True,blank=True)
    job_experience=models.TextField(null=True,blank=True)
    
    def save(self, *args,**kwrgs):
        if not self.slug:
            self.slug = slugify(self.job_title)
        if not self.job_description:
            self.job_description="Job decription will be updated soon please contact the recruiter"
        if not self.job_requirement:
            self.job_requirement="Job Requirements will be updated soon please contace the recruiter"
        return super(Job,self).save(*args,**kwrgs)
    def __str__(self):
        return self.job_title
# class Application(models.Model):
#     applicant_name=models.CharField(max_length=200)
#     applicant_