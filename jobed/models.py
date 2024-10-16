from django.db import models
from django.contrib.auth.models import *
# Create your models here.
class CustomModel(AbstractUser):
    mobile_number = models.IntegerField()
    profile_photo=models.ImageField(upload_to="profile_images")