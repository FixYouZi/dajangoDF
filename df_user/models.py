from django.db import models


# Create your models here.
class UserInfo(models.Model):
    user_name = models.CharField(max_length=50)
    pwd = models.CharField(max_length=40)
    uemail = models.EmailField()
    ushou = models.CharField(max_length=20, default='')
    uaddress = models.CharField(max_length=100, default='')
    uyoubian = models.CharField(max_length=6, default='')
    uphone = models.CharField(max_length=11, default='')
